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
    if 1 == 1 then
        (x y) z
    else
        2 + x
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

result = parse.parse_const(parse.Cursor(cooked))

error_printer = errors.SimpleErrorPrinter()
for error in result.errors:
    error_printer.print_error(error)

print("Parsed AST:")
nodes.ASTPrinter().print_node(result.value)