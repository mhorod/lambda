from lmd.ast.nodes import *


class Visitor:
    '''
    Base class for AST visitors.
    '''

    def visit(self, node):
        CLASS_TO_VISIT_METHOD = {
            ProgramNode: self.visit_program_node,
            ModNode: self.visit_mod_node,
            TokenNode: self.visit_token_node,
            QualifiedIdentifierNode: self.visit_qualified_identifier_node,
            QualifiedTypeNode: self.visit_qualified_type_node,
            PubNode: self.visit_pub_node,
            UseNode: self.visit_use_node,
            ConstNode: self.visit_const_node,
            FnNode: self.visit_fn_node,
            LetNode: self.visit_let_node,
            ExpressionNode: self.visit_expression_node,
            ParenthesisedExpressionNode: self.visit_parenthesised_expression_node,
            BinaryExpressionNode: self.visit_binary_expression_node,
            FunctionCallNode: self.visit_function_call_node,
            IfNode: self.visit_if_node,
        }
        if type(node) in CLASS_TO_VISIT_METHOD:
            return CLASS_TO_VISIT_METHOD[type(node)](node)
        else:
            return self.visit_unknown_node(node)

    def visit_program_node(self, node):
        for statement in node.statements:
            self.visit(statement)

    def visit_mod_node(self, node):
        self.visit(node.name)
        for statement in node.statements:
            self.visit(statement)

    def visit_token_node(self, node):
        return NotImplemented

    def visit_qualified_identifier_node(self, node):
        for part in node.path:
            self.visit(part)

    def visit_qualified_type_node(self, node):
        for part in node.path:
            self.visit(part)

    def visit_pub_node(self, node):
        self.visit(node.node)

    def visit_use_node(self, node):
        self.visit(node.path)

    def visit_const_node(self, node):
        for name in node.names:
            self.visit(name)
        self.visit(node.value)

    def visit_let_node(self, node):
        self.visit(node.name)
        self.visit(node.value)
        self.visit(node.body)

    def visit_fn_node(self, node):
        self.visit(node.name)
        for param in node.params:
            self.visit(param)
        self.visit(node.body)

    def visit_expression_node(self, node):
        for node in node.nodes:
            self.visit(node)

    def visit_parenthesised_expression_node(self, node):
        self.visit(node.expression)

    def visit_binary_expression_node(self, node):
        self.visit(node.left)
        self.visit(node.operator)
        self.visit(node.right)

    def visit_function_call_node(self, node):
        self.visit(node.function)
        for arg in node.arguments:
            self.visit(arg)

    def visit_if_node(self, node):
        self.visit(node.condition)
        self.visit(node.then_branch)
        self.visit(node.else_branch)

    def visit_unknown_node(self, node):
        return NotImplemented
