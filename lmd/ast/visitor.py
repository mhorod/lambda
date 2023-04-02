from lmd.ast.nodes import *


class Visitor:
    '''
    Base class for AST visitors.
    '''

    def visit(self, node):
        if isinstance(node, ProgramNode):
            return self.visit_program_node(node)
        elif isinstance(node, TokenNode):
            return self.visit_token_node(node)
        elif isinstance(node, ConstNode):
            return self.visit_const_node(node)
        elif isinstance(node, LetNode):
            return self.visit_let_node(node)
        elif isinstance(node, ExpressionNode):
            return self.visit_expression_node(node)
        elif isinstance(node, BinaryExpressionNode):
            return self.visit_binary_expression_node(node)
        elif isinstance(node, FunctionCallNode):
            return self.visit_function_call_node(node)
        elif isinstance(node, IfNode):
            return self.visit_if_node(node)
        else:
            return self.visit_unknown_node(node)

    def visit_program_node(self, node):
        return NotImplemented

    def visit_token_node(self, node):
        return NotImplemented

    def visit_const_node(self, node):
        return NotImplemented

    def visit_let_node(self, node):
        return NotImplemented

    def visit_expression_node(self, node):
        return NotImplemented

    def visit_binary_expression_node(self, node):
        return NotImplemented

    def visit_function_call_node(self, node):
        return NotImplemented

    def visit_if_node(self, node):
        return NotImplemented

    def visit_unknown_node(self, node):
        return NotImplemented
