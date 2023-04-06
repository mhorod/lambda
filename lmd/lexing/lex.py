'''
Split source code into raw tokens.
This is the first step before actual parsing, no errors are reported here.
'''

import string

from lmd.util.source import *
from lmd.lexing.cursor import Cursor
from lmd.lexing.raw_token import *


def lex_source(src: Source) -> list:
    '''
    Lex a source in to a list of raw tokens.
    '''

    # predicate: (lookahead, lexer)
    predicate_to_lexer = {
        is_space: (1, lex_whitespace),
        is_comment_start: (2, lex_comment),
        is_digit: (1, lex_number),
        is_name_start: (1, lex_name),
        is_symbol: (1, lex_symbol),
        is_string_start: (1, lex_string),
    }

    result = []
    cursor = Cursor(src)
    while cursor.has():
        for predicate, (lookahead, lexer) in predicate_to_lexer.items():
            if predicate(cursor.peek(lookahead)):
                result.append(lexer(cursor))
                break
        else:
            result.append(lex_unknown(cursor))
    return result


def is_space(s: str) -> bool:
    return s in " \t\r\n"


def is_digit(s: str) -> bool:
    return s in "0123456789"


def is_name_start(s: str) -> bool:
    return s.isalpha() or s == "_" or s == '\''


def is_name_continue(s: str) -> bool:
    return is_name_start(s) or is_digit(s)


def is_string_start(s: str) -> bool:
    return s == '"'


def is_comment_start(s: str) -> bool:
    return s == "--" or s == "{-"


def lex_whitespace(cursor: Cursor) -> Token:
    '''
    Lex whitespace
    '''
    text = ""
    while cursor.has() and is_space(cursor.peek()):
        text += cursor.take()
    return Token(cursor.consume_span(), Whitespace(), text)


def lex_comment(cursor: Cursor) -> Token:
    '''
    Lex a comment
    '''
    if cursor.peek(2) == "--":
        return lex_line_comment(cursor)
    else:
        return lex_block_comment(cursor)


def lex_line_comment(cursor: Cursor) -> Token:
    '''
    Lex a line comment
    '''
    text = cursor.take_while(lambda s: s != "\n")
    span = cursor.consume_span()
    return Token(span, LineComment(), text)


def lex_block_comment(cursor: Cursor) -> Token:
    '''
    Lex a block comment
    '''
    text = ""
    depth = 0
    terminated = False

    while cursor.has():
        if cursor.peek(2) == "{-":
            depth += 1
            text += cursor.take(2)
        elif cursor.peek(2) == "-}":
            depth -= 1
            text += cursor.take(2)
            if depth == 0:
                terminated = True
                break
        else:
            text += cursor.take()

    span = cursor.consume_span()
    return Token(span, BlockComment(terminated), text)


PREFIX_TO_BASE = {
    "0b": 2,
    "0o": 8,
    "0x": 16,
}

NUMBER_CHARACTERS = "_" + string.digits + \
    string.ascii_lowercase + string.ascii_uppercase


def lex_number(cursor: Cursor) -> Token:
    '''
    Lex a number
    '''

    def should_take(cursor: Cursor) -> bool:
        if not cursor.has():
            return False
        elif cursor.peek() in NUMBER_CHARACTERS:
            return True
        elif cursor.peek() == ".":
            if cursor.has(2):
                return cursor.peek(2)[1] in NUMBER_CHARACTERS
            else:
                return False
        else:
            return False

    text = ""
    prefix = cursor.peek(2)
    if prefix in PREFIX_TO_BASE:
        base = PREFIX_TO_BASE[prefix]
        text += cursor.take(2)
    else:
        base = 10

    while should_take(cursor):
        text += cursor.take()

    span = cursor.consume_span()
    return Token(span, Number(base), text)


def lex_name(cursor: Cursor) -> Token:
    '''
    Lex a name
    '''
    text = cursor.take_while(is_name_continue)
    span = cursor.consume_span()
    return Token(span, Name(), text)


DELIMITERS = "()[]{}"
STRUCTURAL_SYMBOLS = ":,;"

MATH_SYMBOLS = "+-*/%&|^~"
COMPARISON_SYMBOLS = "<=>"
MISC_SYMBOLS = "$."
OPERATOR_SYMBOLS = MATH_SYMBOLS + COMPARISON_SYMBOLS + MISC_SYMBOLS

SYMBOLS = DELIMITERS + STRUCTURAL_SYMBOLS + OPERATOR_SYMBOLS


def is_delimiter(s: str) -> bool:
    return s in DELIMITERS


def is_operator(s: str) -> bool:
    return s in OPERATOR_SYMBOLS


def is_symbol(s: str) -> bool:
    return s in SYMBOLS


def lex_symbol(cursor: Cursor) -> Token:
    '''
    Lex a symbol
    '''
    if is_operator(cursor.peek()):
        text = cursor.take_while(is_operator)
        kind = Operator()
    elif is_delimiter(cursor.peek()):
        text = cursor.take()
        kind = Delimiter()
    else:
        text = cursor.take()
        kind = Symbol()
    span = cursor.consume_span()
    return Token(span, kind, text)


def lex_string(cursor: Cursor) -> Token:
    '''
    Lex a string
    '''
    text = cursor.take()
    terminated = False
    while cursor.has():
        c = lex_escaped(cursor)
        text += c
        if c == "\"":
            terminated = True
            break
    span = cursor.consume_span()
    return Token(span, String(terminated), text)


ESCAPED = {"\\n": "\n", "\\r": "\r", "\\t": "\t", "\\\"": "\"", "\\\\": "\\"}


def lex_escaped(cursor: Cursor) -> str:
    '''
    Lex an escaped character
    '''
    if cursor.peek(2) in ESCAPED:
        return cursor.take(2)
    else:
        return cursor.take()


def lex_unknown(cursor: Cursor) -> Token:
    '''
    Lex an unknown token
    '''
    text = cursor.take()
    span = cursor.consume_span()
    return Token(span, Unknown(), text)
