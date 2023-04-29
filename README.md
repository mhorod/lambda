![lambda](logo.png)

---

Small functional language inspired by haskell and rust, made as a fun side
project.

# Usage

To execute a lambda program simply run

```
python3 main.py file.lmd
```

if the file depends on other files you need to add them to the list of sources

```
python3 main.py file1.lmd file2.lmd
```

Interpreter searches for the `main` function and executes it.

# Syntax

```ebnf
name start = lowercase | uppercase | "_" | "'" ;
name continue = name start | decimal digit ;

number = 
    decimal digit+
    "0b", binary digit+ |
    "0o", octal digit+ |
    "0x", hex digit+ | 
    decimal digit+, ".", decimal digit+ ;

literal = number | string ;

line comment = "--", any* ;
block comment = "{-", any*, "-}" ;
whitespace = ( " " | "\t" | "\n" )* ;
identifier = name start, name continue* ;
type = uppercase, name continue* ;

qualified identifier = (type, (".", type)*)?, identifier ;
qualified type = type, (".", type)* ;

math symbol = "+" | "-" | "*" | "/" | "%" | "&" | "|" | "^" | "~" ;
comparison symbol = "<" | "=" | ">" ;
misc symbol = "$" | "." ;
operator = (math symbol | comparison symbol | misc symbol)+ -"." ;


program = statement* ;
statement = use | mod | const ;

use = "use", qualified type ;
mod = "mod", type, "{", statement*, "}" ;

const = "pub"?, "const", identifier+, "=" expr ;
expr = term+, (operator, term+)* ;
term = 
    qualified identifier |
    literal |
    if expr |
    fn expr |
    parenthesised expr ;

if expr = "if", expr, "then", expr, "else", expr ;
fn expr = "fn", identifier+, "=>" expr ;
parenthesised expr = "(", expr, ")" ;
```

# Modules

To allow encapsulation and avoid name collisions lambda has modules, defined by
keyword `mod`. Every `const` declaration can be defined public to be visible
when using this module with the `use` keyword.

Everything (including modules) is contained in the `Main` module. Each module
can see only contents contained in it, unless explicitly uses another module.
