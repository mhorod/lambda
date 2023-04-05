from enum import Enum, auto
from dataclasses import dataclass

from lmd.tokens import *
from lmd.ast.nodes import *
from lmd.ast.transformer import ASTTransformer
from lmd.errors import *


class Associativity(Enum):
    NONE = auto()
    LEFT = auto()
    RIGHT = auto()


@dataclass
class Precedence:
    priority: int
    associativity: Associativity


class ExpressionTransformer(ASTTransformer):
    def __init__(self, precedence_table):
        self.precedence_table = precedence_table
        self.failed = False

    def transform(self, ast, report):
        self.error_report = report
        self.failed = False
        return self.visit(ast)

    def visit_expression_node(self, node):
        self.failed = False
        nodes = [self.visit(child) for child in node.nodes]
        return self.parse_expr(nodes, None)[0]

    def parse_expr(self, nodes, last_operator):
        '''
        Parse right-hand side of the {last_operator} operator.
        Parses all operators that bind more tightly than {last_operator}.
        '''
        node, nodes = self.parse_term(nodes)
        previous_operator = last_operator

        while (not self.failed and nodes and self.right_op_first(last_operator, nodes[0])):
            operator = nodes[0]
            nodes = nodes[1:]

            if operator.token.text not in self.precedence_table:
                self.unknown_operator(operator)
                return None, None

            rhs, nodes = self.parse_expr(nodes, previous_operator)
            node = BinaryExpressionNode(node, operator, rhs)
            previous_operator = operator
        return node, nodes

    def parse_term(self, nodes):
        i = 0
        while i < len(nodes) and not self.is_operator(nodes[i]):
            i += 1

        args, nodes = nodes[:i], nodes[i:]
        if len(args) == 1:
            return args[0], nodes
        elif len(args) >= 2:
            node = FunctionCallNode(args[0], args[1:])
            return node, nodes

    def is_operator(self, node):
        return isinstance(node, TokenNode) and node.token.kind.extends(Operator())

    def right_op_first(self, left, right):
        '''
        Returns true if expression of form x {left} y {right} z
        evaluates to x {left} (y {right} z).

        This happens when {right} binds more tightly than {left}.
        or they are the same right-associative operator
        '''
        if left is None:
            return True

        left_op = left.token.text
        right_op = right.token.text

        if right_op not in self.precedence_table:
            self.unknown_operator(right)
            return False

        if left_op == right_op:
            return self.precedence_table[left_op].associativity == Associativity.RIGHT
        else:
            return self.precedence_table[left_op].priority < self.precedence_table[right_op].priority

    def unknown_operator(self, node):
        message = Message(node.span, f"Unknown operator: `{node.token.text}`")
        error = Error(message)
        self.error_report.add(error)
        self.failed = True
