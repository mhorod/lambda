from typing import List

from lmd.util.source import Span, wrapping_span
from lmd.util.token import Token


class Node:
    def __init__(self, span: Span):
        self.span = span

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__


class ProgramNode(Node):
    def __init__(self, span: Span, statements):
        super().__init__(span)
        self.statements = statements

    def __repr__(self):
        return f"program ({self.statements})"


class ModNode(Node):
    def __init__(self, span: Span, name: Node, statements):
        super().__init__(span)
        self.name = name
        self.statements = statements

    def __repr__(self):
        return f"mod ({self.name}) ({self.statements})"


class TokenNode(Node):
    def __init__(self, token: Token):
        super().__init__(token.span)
        self.token = token

    def __repr__(self):
        return f"token ({self.token})"


class QualifiedIdentifierNode(Node):
    def __init__(self, span: Span, path: List[str]):
        super().__init__(span)
        self.path = path

    def __repr__(self):
        return f"qualified identifier ({self.path})"


class QualifiedTypeNode(Node):
    def __init__(self, span: Span, path: List[str]):
        super().__init__(span)
        self.path = path

    def __repr__(self):
        return f"qualified type ({self.path})"


class PubNode(Node):
    def __init__(self, span, node):
        super().__init__(span)
        self.node = node

    def __repr__(self):
        return f"pub ({self.node})"


class UseNode(Node):
    def __init__(self, span: Span, path: Node):
        super().__init__(span)
        self.path = path

    def __repr__(self):
        return f"use ({self.path})"


class ConstNode(Node):
    def __init__(self, span: Span, names: list, value: Node):
        super().__init__(span)
        self.names = names
        self.value = value

    def __repr__(self):
        return f"const ({self.names}) = ({self.value})"


class FnNode(Node):
    def __init__(self, span: Span, args: list, body: Node):
        super().__init__(span)
        self.args = args
        self.body = body

    def __repr__(self):
        return f"fn ({self.args}) => ({self.body})"


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
        spans = [node.span for node in nodes if node is not None]
        span = None if len(spans) == 0 else wrapping_span(spans)
        super().__init__(span)
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
