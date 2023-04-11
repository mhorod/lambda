from lmd.ast.visitor import Visitor
from lmd.ast.nodes import *


class ASTTransformer(Visitor):
    '''
    Special kind of visitor that transforms the AST into a new AST.
    Default implementation just traverses the tree and returns the same nodes.
    '''

    def visit_program_node(self, node):
        return ProgramNode(node.span, [self.visit(statement) for statement in node.statements])

    def visit_token_node(self, node):
        return node

    def visit_pub_node(self, node):
        return PubNode(self.visit(node.node))

    def visit_const_node(self, node):
        return ConstNode(node.span, self.visit(node.name), self.visit(node.value))

    def visit_let_node(self, node):
        return LetNode(node.span, self.visit(node.name), self.visit(node.value), self.visit(node.body))

    def visit_expression_node(self, node):
        return ExpressionNode(self.visit(node.nodes))

    def visit_parenthesised_expression_node(self, node):
        return ParenthesisedExpressionNode(node.span, self.visit(node.expression))

    def visit_binary_expression_node(self, node):
        return BinaryExpressionNode(self.visit(node.left), self.visit(node.operator), self.visit(node.right))

    def visit_function_call_node(self, node):
        return FunctionCallNode(self.visit(node.function), self.visit(node.arguments))

    def visit_if_node(self, node):
        return IfNode(
            node.span,
            self.visit(node.condition),
            self.visit(node.true_branch),
            self.visit(node.false_branch)
        )

    def visit_unknown_node(self, node):
        return node
