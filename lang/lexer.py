from lang.cursor import Cursor
from lang.tokens import *


def lex_program(text):
    cursor = Cursor(text)
    tokens = []
    while cursor.has():
        token = None
        if is_identifier(cursor.peek()):
            token = lex_identifier(cursor)
        elif cursor.peek().isdigit():
            token = lex_number(cursor)
        elif cursor.peek() == '\"':
            token = lex_string(cursor)
        elif cursor.peek().isspace():
            skip_whitespace(cursor)
            if cursor.peek() == '\n':
                cursor.skip()
            continue
        elif cursor.peek(2) == '--':
            lex_comment(cursor)
            continue
        else:
            token = lex_symbol(cursor)

        if token is not None:
            tokens.append(token)
        else:
            print("error while lexing:", cursor.peek())
            break
    return tokens


def is_identifier(c):
    return c.isalpha() or c == '_' or c == '\''


def lex_identifier(cursor):
    identifier = ""
    while cursor.has() and is_identifier(cursor.peek()):
        identifier += cursor.peek()
        cursor.skip()
    return Identifier(identifier)


def lex_number(cursor):
    number = ""
    while cursor.has() and cursor.peek().isdigit():
        number += cursor.peek()
        cursor.skip()
    return Number(number)


def lex_string(cursor):
    cursor.skip()  # "
    text = ""
    while cursor.has() and cursor.peek() != "\"":
        text += lex_char(cursor)
    cursor.skip()  # "
    return String(text)


def lex_char(cursor):
    if cursor.peek() == "\\":
        return cursor.consume(2)
    else:
        return cursor.consume()


def lex_comment(cursor):
    text = ""
    cursor.skip(2)  # --
    while cursor.peek() != '\n':
        text += cursor.peek()
        cursor.skip()
    return Comment(text)


def skip_whitespace(cursor):
    while cursor.has() and cursor.peek().isspace() and cursor.peek() != '\n':
        cursor.skip()


def lex_symbol(cursor):
    parens = '()[]{}'
    math = ['+', '-', '*', '/', '//']
    ops = ['!=', '==', '=', '<', '>', '<=', '>=']
    other = [';', ',', '#', '::', ':', '=>', '->']
    symbols = list(parens) + list(math) + list(ops) + list(other)
    count = 0
    while cursor.has() and cursor.peek(count + 1) in symbols:
        count += 1

    if count == 0: return None
    symbol = Symbol(cursor.peek(count))

    cursor.skip(count)
    return symbol
