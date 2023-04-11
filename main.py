from lmd import *

source_code = """
const x = 1
-- nested comment
{- const y = 2 {- -} -}
const a = if x == 1 then 1 else 2
const z = "hello\\n"
const w = "world"
"""

source_code = """
pub const x = 1
const x =
    if x + y == 1 then
        if true then
            2 + (x y) $ z w * 1
        else
            0b0
    else
        (_ + x)
"""


class Pipeline:
    def __init__(self):
        self.phases = []

    def then(self, phase):
        self.phases.append(phase)
        return self

    def run(self, initial_value, error_printer):
        value = initial_value
        report = util.error.ErrorReport()
        for phase in self.phases:
            value = phase(value, report)
            if report.has_errors():
                error_printer.print_error_report(report)
                return value
        return value


def lex_source(source, _):
    return lexing.lex.lex_source(source)


def filter_whitespace(cooked_tokens, _):
    return [token for token in cooked_tokens
            if not token.kind.extends(tokens.Comment())
            and not token.kind.extends(tokens.Whitespace())]


def transform_expressions(transformer):
    def f(ast, report):
        return transformer.transform(ast, report)
    return f


src = util.source.Source("main", source_code)

precedence_table = {
    '$': ast.expressions.Precedence(0, ast.expressions.Associativity.LEFT),
    '==': ast.expressions.Precedence(4, ast.expressions.Associativity.LEFT),
    '+': ast.expressions.Precedence(6, ast.expressions.Associativity.LEFT),
    '*': ast.expressions.Precedence(7, ast.expressions.Associativity.LEFT),
}

expression_transformer = ast.expressions.ExpressionTransformer(
    precedence_table)
error_printer = output.error.SimpleErrorPrinter()

pipeline = Pipeline()\
    .then(lex_source)\
    .then(cooking.cook.cook_tokens)\
    .then(filter_whitespace)\
    .then(parsing.parse.parse_tokens)\
    .then(transform_expressions(expression_transformer))\


parsed = pipeline.run(src, error_printer)
ast_printer = output.ast.ASTPrinter()
ast_printer.visit(parsed)
