from lmd import *

source_code = """
let x = 1
-- nested comment
{- let y = 2 {- -} -}
let z = "hello\\n"
let w = "world
"""

src = source.Source("main", source_code)

tokens = lex.lex_source(src)

for token in tokens:
    print(token)
print()

report = errors.ErrorReport()
cooked = cook.cook_tokens(tokens, report)
errors.SimpleErrorPrinter().print(report)

print()

for token in cooked:
    print(token)
