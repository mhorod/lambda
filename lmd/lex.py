'''
Split source code into raw tokens.
This is the first step before actual parsing, no errors are reported here.
'''

from dataclasses import dataclass, field
from enum import Enum, auto

from lmd import source


class Cursor:
    '''
    Cursor that points to a position in a source.
    '''

    def __init__(self, src: source.Source, index: int = 0):
        self.src = src
        self.index = index
        self.consumed_begin = index

    def peek(self, cnt: int = 1) -> str:
        '''
        Peek at the next `cnt` characters
        '''
        return self.src[self.index:self.index + cnt]

    def take(self, cnt: int = 1) -> str:
        '''
        Take the next `cnt` characters
        '''
        result = self.peek(cnt)
        self.index += cnt
        return result

    def take_while(self, predicate) -> str:
        '''
        Take characters while `predicate` returns true
        '''
        result = ""
        while self.has() and predicate(self.peek()):
            result += self.take()
        return result

    def has(self, cnt: int = 1) -> bool:
        '''
        Check if there are `cnt` characters left
        '''
        return self.index + cnt <= self.src.len()

    def consume_span(self) -> source.Span:
        '''
        Consume the span from the last `consume_span` call to now.
        '''
        result = source.Span(self.src, self.consumed_begin, self.index)
        self.consumed_begin = self.index
        return result


class TokenGroup(Enum):
    '''
    Group that token belongs to.
    '''
    WHITESPACE = auto()
    COMMENT = auto()
    LITERAL = auto()
    NAME = auto()
    DELIMITER = auto()
    OPERATOR = auto()
    SYMBOL = auto()
    UNKNOWN = auto()


class LiteralType(Enum):
    '''
    Type of literal.
    '''
    STRING = auto()
    NUMBER = auto()


class RawToken:
    '''
    A raw token, not yet parsed.
    '''
    span: source.Span
    group: TokenGroup
    text: str

    def __init__(self, span: source.Span, group: TokenGroup, text: str, **kwargs):
        self.span = span
        self.group = group
        self.text = text
        for k, v in kwargs.items():
            if not isinstance(k, str):
                raise TypeError("extra keys must be strings")
            else:
                setattr(self, k, v)

    def __str__(self):
        extra = ", ".join(
            f"{k}={getattr(self, k)}" for k in self.extra_attrs())
        if extra:
            extra = " " + extra
        return f'{self.span}: {self.group.name} {repr(self.text)}{extra}'

    def extra_attrs(self):
        return [k for k in self.__dict__.keys() if k not in ["span", "group", "text"] and not k.startswith("_")]


def lex_source(src: source.Source) -> list:
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


def lex_whitespace(cursor: Cursor) -> RawToken:
    '''
    Lex whitespace
    '''
    content = ""
    while cursor.has() and is_space(cursor.peek()):
        content += cursor.take()
    return RawToken(cursor.consume_span(), TokenGroup.WHITESPACE, content)


def lex_comment(cursor: Cursor) -> RawToken:
    '''
    Lex a comment
    '''
    if cursor.peek(2) == "--":
        return lex_line_comment(cursor)
    else:
        return lex_block_comment(cursor)


def lex_line_comment(cursor: Cursor) -> RawToken:
    '''
    Lex a line comment
    '''
    content = cursor.take_while(lambda s: s != "\n")
    span = cursor.consume_span()
    return RawToken(span, TokenGroup.COMMENT, content, terminated=True)


def lex_block_comment(cursor: Cursor) -> RawToken:
    '''
    Lex a block comment
    '''
    content = ""
    depth = 0
    terminated = False

    while cursor.has():
        if cursor.peek(2) == "{-":
            depth += 1
            content += cursor.take(2)
        elif cursor.peek(2) == "-}":
            depth -= 1
            content += cursor.take(2)
            if depth == 0:
                terminated = True
                break
        else:
            content += cursor.take()

    span = cursor.consume_span()
    return RawToken(span, TokenGroup.COMMENT, content, terminated=terminated)


def lex_number(cursor: Cursor) -> RawToken:
    '''
    Lex a number
    '''
    content = cursor.take_while(is_digit)
    span = cursor.consume_span()
    return RawToken(span, TokenGroup.LITERAL, content, type=LiteralType.NUMBER)


def lex_name(cursor: Cursor) -> RawToken:
    '''
    Lex a name
    '''
    content = cursor.take_while(is_name_continue)
    span = cursor.consume_span()
    return RawToken(span, TokenGroup.NAME, content)


DELIMITERS = "()[]{}"
STRUCTURAL_SYMBOLS = ":,;."

MATH_SYMBOLS = "+-*/%&|^~"
COMPARISON_SYMBOLS = "<=>"
OPERATOR_SYMBOLS = MATH_SYMBOLS + COMPARISON_SYMBOLS

SYMBOLS = DELIMITERS + STRUCTURAL_SYMBOLS + OPERATOR_SYMBOLS


def is_delimiter(s: str) -> bool:
    return s in DELIMITERS


def is_operator(s: str) -> bool:
    return s in OPERATOR_SYMBOLS


def is_symbol(s: str) -> bool:
    return s in SYMBOLS


def lex_symbol(cursor: Cursor) -> RawToken:
    '''
    Lex a symbol
    '''
    if is_operator(cursor.peek()):
        content = cursor.take_while(is_operator)
        group = TokenGroup.OPERATOR
    elif is_delimiter(cursor.peek()):
        content = cursor.take()
        group = TokenGroup.DELIMITER
    else:
        content = cursor.take()
        group = TokenGroup.SYMBOL
    span = cursor.consume_span()
    return RawToken(span, group, content)


def lex_string(cursor: Cursor) -> RawToken:
    '''
    Lex a string
    '''
    content = cursor.take()
    terminated = False
    while cursor.has():
        c = lex_escaped(cursor)
        content += c
        if c == "\"":
            terminated = True
            break
    span = cursor.consume_span()
    return RawToken(span, TokenGroup.LITERAL, content, type=LiteralType.STRING, terminated=terminated)


ESCAPED = {"\\n": "\n", "\\r": "\r", "\\t": "\t", "\\\"": "\"", "\\\\": "\\"}


def lex_escaped(cursor: Cursor) -> str:
    '''
    Lex an escaped character
    '''
    if cursor.peek(2) in ESCAPED:
        return ESCAPED[cursor.take(2)]
    else:
        return cursor.take()


def lex_unknown(cursor: Cursor) -> RawToken:
    '''
    Lex an unknown token
    '''
    content = cursor.take()
    span = cursor.consume_span()
    return RawToken(span, TokenGroup.UNKNOWN, content)
