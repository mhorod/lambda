class TokenNode:
    def __init__(self, token):
        self.token = token

    def __repr__(self):
        return f"token ({self.token})"

class ConstNode:
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def __repr__(self):
        return f"const ({self.name}) = ({self.value})"


class ExpressionNode:
    def __init__(self, nodes):
        self.nodes = nodes

    def __repr__(self):
        return f"expr ({self.nodes})"

class IfNode:
    def __init__(self, condition, true_branch, false_branch):
        self.condition = condition
        self.true_branch = true_branch
        self.false_branch = false_branch

class ASTPrinter:
    def __init__(self):
        self.depth = 0

    def indent(self):
        self.depth += 1

    def unindent(self):
        self.depth -= 1

    def print(self, x):
        print("  " * self.depth + str(x))

    def print_node(self, node):
        if isinstance(node, TokenNode):
            return self.print_token_node(node)
        elif isinstance(node, ConstNode):
            return self.print_const_node(node)
        elif isinstance(node, ExpressionNode):
            return self.print_expression_node(node)
        elif isinstance(node, IfNode):
            return self.print_if_node(node)
        else:
            self.print_unknown_node(node)

    def print_unknown_node(self, node):
        self.print("unknown")
        self.indent()
        self.print(repr(node))
        self.unindent()

    def print_token_node(self, node):
        self.print("token")
        self.indent()
        self.print(node.token)
        self.unindent()

    def print_const_node(self, node):
        self.print("const")
        self.indent()
        self.print_node(node.name)
        self.print_node(node.value)
        self.unindent()

    def print_expression_node(self, node):
        self.print("expr")
        self.indent()
        for n in node.nodes:
            self.print_node(n)
        self.unindent()

    def print_if_node(self, node):
        self.print("if")
        self.indent()
        self.print_node(node.condition)
        self.unindent()

        self.print("then")
        self.indent()
        self.print_node(node.true_branch)
        self.unindent()

        self.print("else")
        self.indent()
        self.print_node(node.false_branch)
        self.unindent()