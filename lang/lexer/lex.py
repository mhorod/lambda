from lang.tokens import *
from lang.source import *

from ..result import *
from .cursor import Cursor
from lang.error import Error


def lex_program(source: Source):
    cursor = Cursor(source)
    result = Ok(cursor, [])
    while result.is_ok() and result.cursor.has():
        if is_identifier_start(result.cursor.peek()):
            result = result.and_then(lex_identifier)
        elif result.cursor.peek().isdigit():
            result = result.and_then(lex_number)
        elif result.cursor.peek() == '\"':
            result = result.and_then(lex_string)
        elif result.cursor.peek().isspace():
            result = result.and_then(lex_whitespace)
        elif result.cursor.peek(2) == '--':
            result = result.and_then(lex_comment)
        else:
            result = result.and_then(lex_symbol)
    return result


def is_identifier_start(c):
    return c.isalpha() or c == '_' or c == '\''


def is_identifier_continue(c):
    return c.isalpha() or c == '_' or c == '\'' or c.isdigit()


def lex_identifier(cursor):
    """
    lex an identifier i.e. a sequence of letters, digits, apostrophes or underscores
    """
    return Ok(cursor.clone(), [])\
        .and_then(expect_matches(is_identifier_start, "character, _, or '"))\
        .and_then(take_while(is_identifier_start, 1))\
        .and_then(take_while(is_identifier_continue))\
        .and_then_transform(lambda cursor, tokens: Ok(cursor, Identifier(tokens[0] + tokens[1], cursor.consumed_location())))


def lex_number(cursor):
    '''
    lex a decimal number
    '''
    return Ok(cursor.clone(), [])\
        .and_then(expect_matches(lambda c: c.isdigit()))\
        .and_then(take_while(lambda c: c.isdigit()))\
        .and_then_transform(lambda cursor, tokens: Ok(cursor, Number(tokens[0], cursor.consumed_location())))


def lex_string(cursor):
    '''
    lex a string with escaped characters
    '''

    def expect_has(cursor):
        if cursor.has():
            return Ok(cursor, [])
        else:
            error = Error("unexpected end of file while lexing string",
                          cursor.consumed_location())
            return Err(cursor, error, True)

    return Ok(cursor.clone(), [])\
        .and_then(expect_and_skip('\"'))\
        .and_then(lex_anything_until_quote)\
        .and_then(expect_has)\
        .and_then(expect_and_skip('\"'))\
        .and_then_transform(lambda cursor, tokens: Ok(cursor, String(tokens[0], cursor.consumed_location())))


def lex_anything_until_quote(cursor):
    text = ""
    while cursor.has() and cursor.peek() != "\"":
        text += lex_char(cursor)
    return Ok(cursor, text)


def lex_char(cursor):
    '''
    lex a single character
    '''
    if cursor.peek() == "\\":
        return cursor.take(2)
    else:
        return cursor.take()


def lex_comment(cursor):
    '''
    lex a comment, a line starting with --
    '''
    return Ok(cursor, [])\
        .and_then(expect_and_skip("--"))\
        .and_then(take_while(lambda c: c != '\n'))\
        .and_then_transform(lambda cursor, tokens: Ok(cursor, Comment(tokens[0], cursor.consumed_location())))


def lex_whitespace(cursor):
    cursor = cursor.clone()
    text = cursor.take_while(lambda c: c.isspace())
    return Ok(cursor, Whitespace(text, cursor.consumed_location()))


def lex_symbol(cursor):
    parens = '()[]{}'
    math = ['+', '-', '*', '/', '//']
    ops = ['!=', '==', '=', '<', '>', '<=', '>=']
    other = [';', ',', '#', '::', ':', '=>', '->']
    symbols = list(parens) + list(math) + list(ops) + list(other)

    cursor = cursor.clone()
    count = 0
    while cursor.has(count + 1) and cursor.peek(count + 1) in symbols:
        count += 1

    if count == 0:
        return Err(cursor, "unrecognized symbol", False)

    text = cursor.take(count)
    symbol = Symbol(text, cursor.consumed_location())
    return Ok(cursor, symbol)


# Cursor functions that can be plugged into result and_then

def expect_and_skip(expected):
    def transform(cursor, tokens):
        if len(tokens) == 1 and tokens[0] == expected:
            return Ok(cursor, [])
        else:
            error = Error("expected " + expected,
                          cursor.consumed_location())
            return Err(cursor, error, True)

    def f(cursor):
        return Ok(cursor.clone(), []).and_then(take(len(expected))).and_then_transform(transform)
    return f


def expect_matches(predicate, expected=None):
    '''
    expect a sequence of characters that match a predicate without consuming them
     '''
    def transform(cursor, tokens):
        if len(tokens) == 1 and predicate(tokens[0]):
            return Ok(cursor, [])
        else:
            msg = "" if expected is None else ", expected " + expected
            error = Error("unexpected character: " +
                          cursor.peek() + msg, cursor.consumed_location())
            return Err(cursor, error, True)

    def f(cursor):
        return Ok(cursor, []).and_then(peek_while(predicate, 1)).and_then_transform(transform)

    return f


def take(count):
    def f(cursor):
        if count > cursor.remaining():
            return Err(cursor, "EOF reached while lexing", True)
        else:
            return Ok(cursor, cursor.take(count))
    return f


def take_while(predicate, limit=None):
    def f(cursor):
        return Ok(cursor, cursor.take_while(predicate, limit))
    return f


def peek_while(predicate, limit=None):
    def f(cursor):
        return Ok(cursor, cursor.peek_while(predicate, limit))
    return f
