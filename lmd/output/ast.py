from lmd.ast.visitor import Visitor
from lmd.ast.nodes import *


class ASTPrinter(Visitor):
    def __init__(self):
        self.depth = 0

    def indent(self):
        self.depth += 1

    def unindent(self):
        self.depth -= 1

    def print(self, x):
        print("  " * self.depth + str(x))

    def visit_unknown_node(self, node):
        self.print("unknown")
        self.indent()
        self.print(repr(node))
        self.unindent()

    def visit_program_node(self, node):
        self.print(f"{node.span} program")
        self.indent()
        for n in node.statements:
            self.visit(n)
        self.unindent()

    def visit_token_node(self, node):
        self.print("token")
        self.indent()
        self.print(node.token)
        self.unindent()

    def visit_qualified_identifier_node(self, node):
        self.print(f"{node.span} qualified identifier")
        self.indent()
        for n in node.path:
            self.visit(n)
        self.unindent()

    def visit_pub_node(self, node):
        self.print(f"{node.span} pub")
        self.indent()
        self.visit(node.node)
        self.unindent()

    def visit_const_node(self, node):
        self.print(f"{node.span} const")
        self.indent()
        for n in node.names:
            self.visit(n)
        self.print("=")
        self.visit(node.value)
        self.unindent()

    def visit_fn_node(self, node):
        self.print(f"{node.span} fn")
        self.indent()
        for arg in node.args:
            self.visit(arg)
        self.print("=>")
        self.visit(node.body)
        self.unindent()

    def visit_let_node(self, node):
        self.print("let")
        self.indent()
        self.visit(node.name)
        self.visit(node.value)
        self.unindent()

        self.print("in")
        self.indent()
        self.visit(node.body)
        self.unindent()

    def visit_expression_node(self, node):
        self.print(f"{node.span} expr")
        self.indent()
        for n in node.nodes:
            self.visit(n)
        self.unindent()

    def visit_parenthesised_expression_node(self, node):
        self.print(f"{node.span} paren_expr")
        self.indent()
        self.visit(node.expression)
        self.unindent()

    def visit_binary_expression_node(self, node):
        self.print(f"{node.span} binary")
        self.indent()

        self.print("left")
        self.indent()
        self.visit(node.left)
        self.unindent()

        self.print("operator")
        self.indent()
        self.visit(node.operator)
        self.unindent()

        self.print("right")
        self.indent()
        self.visit(node.right)
        self.unindent()

        self.unindent()

    def visit_function_call_node(self, node):
        self.print(f"{node.span} call")
        self.indent()
        self.visit(node.function)
        for n in node.arguments:
            self.visit(n)
        self.unindent()

    def visit_if_node(self, node):
        self.print(f"{node.span} if")
        self.indent()
        self.visit(node.condition)
        self.unindent()

        self.print("then")
        self.indent()
        self.visit(node.true_branch)
        self.unindent()

        self.print("else")
        self.indent()
        self.visit(node.false_branch)
        self.unindent()
