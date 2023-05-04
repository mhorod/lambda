from lmd.ast.visitor import Visitor
from lmd.modules.error import *


class ModuleTreeBuilder(Visitor):
    def __init__(self):
        self.tree = {
            'Main': {}
        }
        self.tree_stack = [self.tree['Main']]

    def current_tree(self):
        return self.tree_stack[-1]

    def path_node_to_list(self, node):
        return [part.token.text for part in node.path]

    def push(self, path_node):
        path = self.path_node_to_list(path_node)
        tree = self.current_tree()
        for part in path:
            if part not in tree:
                tree[part] = {}
            tree = tree[part]
        self.tree_stack.append(tree)

    def pop(self):
        self.tree_stack.pop()

    def visit_mod_node(self, node):
        self.push(node.name)
        for statement in node.statements:
            self.visit(statement)
        self.pop()

    def visit_pub_node(self, node):
        name = node.node.names[0].token.text
        if name not in self.current_tree():
            self.current_tree()[name] = []
        self.current_tree()[name].append(node)

    def visit_const_node(self, node):
        name = node.names[0].token.text
        if name not in self.current_tree():
            self.current_tree()[name] = []
        self.current_tree()[name].append(node)


def build_module_tree(node):
    builder = ModuleTreeBuilder()
    builder.visit(node)
    return builder.tree


def merge_trees(t1, t2):
    merged = {**t1}
    for k, v in t2.items():
        if k in merged:
            merged[k] = merge_trees(merged[k], v)
        else:
            merged[k] = v
    return merged


def report_multiple_definitions(tree, report):
    for k, v in tree.items():
        if isinstance(v, dict):
            report_multiple_definitions(v, report)
        elif len(v) > 1:
            error = multiple_definitions(v)
            report.add(error)
