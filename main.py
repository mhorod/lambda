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
const x = 
    if x + y == 1 then
        2 + (x y) $ z w * 1
    else
        (_ + x)
"""

source_code = """
const x = 1 + f $ 1
"""

src = source.Source("main", source_code)

lexed = lex.lex_source(src)

print("Lexed tokens:")
for token in lexed:
    print(token)
print()

report = errors.ErrorReport()
cooked = cook.cook_tokens(lexed, report)
errors.SimpleErrorPrinter().print(report)

print()
print("Cooked tokens:")
for token in cooked:
    print(token)

print()
cooked = [token for token in cooked
          if not token.kind.extends(tokens.Comment())
          and not token.kind.extends(tokens.Whitespace())]

result = parse.parse_program(parse.Cursor(cooked))
for error in result.errors:
    report.add(error)


print("Parsed AST:")
printer = ast.nodes.ASTPrinter()
printer.print_node(result.value)

precedence_table = {
    '$': ast.expressions.Precedence(0, ast.expressions.Associativity.LEFT),
    '==': ast.expressions.Precedence(4, ast.expressions.Associativity.LEFT),
    '+': ast.expressions.Precedence(6, ast.expressions.Associativity.LEFT),
    '*': ast.expressions.Precedence(7, ast.expressions.Associativity.LEFT),
}

expression_transformer = ast.expressions.ExpressionTransformer(
    precedence_table, report)
transformed = expression_transformer.visit(result.value)

print("Transformed AST:")
printer.print_node(transformed)

error_printer = errors.SimpleErrorPrinter()
error_printer.print(report)
