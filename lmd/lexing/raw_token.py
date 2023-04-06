
from enum import Enum, auto

from lmd.source import *
from lmd.util.token import *


class RawTokenType(Enum):
    WHITESPACE = auto()
    COMMENT = auto()
    LITERAL = auto()
    NAME = auto()
    DELIMITER = auto()
    OPERATOR = auto()
    SYMBOL = auto()
    UNKNOWN = auto()


class Whitespace(TokenKind):
    def __init__(self):
        super().__init__(RawTokenType.WHITESPACE)


class Name(TokenKind):
    def __init__(self):
        super().__init__(RawTokenType.NAME)


class Delimiter(TokenKind):
    def __init__(self):
        super().__init__(RawTokenType.DELIMITER)


class Operator(TokenKind):
    def __init__(self):
        super().__init__(RawTokenType.OPERATOR)


class Symbol(TokenKind):
    def __init__(self):
        super().__init__(RawTokenType.SYMBOL)


class Unknown(TokenKind):
    def __init__(self):
        super().__init__(RawTokenType.UNKNOWN)


class CommentType(Enum):
    LINE = auto()
    BLOCK = auto()


class Comment(TokenKind):
    def __init__(self, comment_type: CommentType, terminated):
        super().__init__(RawTokenType.COMMENT)
        self.comment_type = comment_type
        self.terminated = terminated


class LineComment(Comment):
    def __init__(self):
        super().__init__(CommentType.LINE, terminated=True)


class BlockComment(Comment):
    def __init__(self, terinated):
        super().__init__(CommentType.BLOCK, terinated)


class LiteralType(Enum):
    STRING = auto()
    NUMBER = auto()


class Literal(TokenKind):
    def __init__(self, literal_type: LiteralType):
        super().__init__(RawTokenType.LITERAL)
        self.literal_type = literal_type


class String(Literal):
    def __init__(self, terminated):
        super().__init__(LiteralType.STRING)
        self.terminated = terminated


class Number(Literal):
    def __init__(self, base):
        super().__init__(LiteralType.NUMBER)
        self.base = base
