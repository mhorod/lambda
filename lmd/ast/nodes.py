from typing import List

from lmd.source import Span, wrapping_span
from lmd.tokens import Token


class Node:
    def __init__(self, span: Span):
        self.span = span


class ProgramNode(Node):
    def __init__(self, span: Span, statements):
        super().__init__(span)
        self.statements = statements

    def __repr__(self):
        return f"program ({self.statements})"


class TokenNode(Node):
    def __init__(self, token: Token):
        super().__init__(token.span)
        self.token = token

    def __repr__(self):
        return f"token ({self.token})"


class ConstNode(Node):
    def __init__(self, span: Span, name: Node, value: Node):
        super().__init__(span)
        self.name = name
        self.value = value

    def __repr__(self):
        return f"const ({self.name}) = ({self.value})"


class LetNode(Node):
    def __init__(self, span: Span, name, value, body):
        super().__init__(span)
        self.name = name
        self.value = value
        self.body = body

    def __repr__(self):
        return f"let ({self.name}) = ({self.value}) in ({self.body})"


class ExpressionNode(Node):
    def __init__(self, nodes: List[Node]):
        super().__init__(wrapping_span([node.span for node in nodes]))
        self.nodes = nodes

    def __repr__(self):
        return f"expr ({self.nodes})"


class ParenthesisedExpressionNode(Node):
    def __init__(self, span: Span, expression: Node):
        super().__init__(span)
        self.expression = expression

    def __repr__(self):
        return f"paren_expr ({self.expression})"


class BinaryExpressionNode(Node):
    def __init__(self, left: Node, operator: Node, right: Node):
        super().__init__(wrapping_span([left.span, operator.span, right.span]))
        self.left = left
        self.operator = operator
        self.right = right


class FunctionCallNode(Node):
    def __init__(self, function: Node, arguments: Node):
        spans = [function.span] + [argument.span for argument in arguments]
        super().__init__(wrapping_span(spans))
        self.function = function
        self.arguments = arguments


class IfNode(Node):
    def __init__(self, span: Span, condition: Node, true_branch: Node, false_branch: Node):
        super().__init__(span)
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
        if isinstance(node, ProgramNode):
            return self.print_program_node(node)
        elif isinstance(node, TokenNode):
            return self.print_token_node(node)
        elif isinstance(node, ConstNode):
            return self.print_const_node(node)
        elif isinstance(node, LetNode):
            return self.print_let_node(node)
        elif isinstance(node, ExpressionNode):
            return self.print_expression_node(node)
        elif isinstance(node, ParenthesisedExpressionNode):
            return self.print_parenthesised_expression_node(node)
        elif isinstance(node, BinaryExpressionNode):
            return self.print_binary_expression_node(node)
        elif isinstance(node, FunctionCallNode):
            return self.print_function_call_node(node)
        elif isinstance(node, IfNode):
            return self.print_if_node(node)
        else:
            self.print_unknown_node(node)

    def print_unknown_node(self, node):
        self.print("unknown")
        self.indent()
        self.print(repr(node))
        self.unindent()

    def print_program_node(self, node):
        self.print(f"{node.span} program")
        self.indent()
        for n in node.statements:
            self.print_node(n)
        self.unindent()

    def print_token_node(self, node):
        self.print("token")
        self.indent()
        self.print(node.token)
        self.unindent()

    def print_const_node(self, node):
        self.print(f"{node.span} const")
        self.indent()
        self.print_node(node.name)
        self.print_node(node.value)
        self.unindent()

    def print_let_node(self, node):
        self.print("let")
        self.indent()
        self.print_node(node.name)
        self.print_node(node.value)
        self.unindent()

        self.print("in")
        self.indent()
        self.print_node(node.body)
        self.unindent()

    def print_expression_node(self, node):
        self.print(f"{node.span} expr")
        self.indent()
        for n in node.nodes:
            self.print_node(n)
        self.unindent()

    def print_parenthesised_expression_node(self, node):
        self.print(f"{node.span} paren_expr")
        self.indent()
        self.print_node(node.expression)
        self.unindent()

    def print_binary_expression_node(self, node):
        self.print(f"{node.span} binary")
        self.indent()

        self.print("left")
        self.indent()
        self.print_node(node.left)
        self.unindent()

        self.print("operator")
        self.indent()
        self.print_node(node.operator)
        self.unindent()

        self.print("right")
        self.indent()
        self.print_node(node.right)
        self.unindent()

        self.unindent()

    def print_function_call_node(self, node):
        self.print(f"{node.span} call")
        self.indent()
        self.print_node(node.function)
        for n in node.arguments:
            self.print_node(n)
        self.unindent()

    def print_if_node(self, node):
        self.print(f"{node.span} if")
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
