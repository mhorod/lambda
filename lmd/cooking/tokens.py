'''
Definition of rich tokens used by the parser
'''

from enum import Enum, auto

from lmd.util.token import TokenKind


class TokenType(Enum):
    COMMENT = auto()
    WHITESPACE = auto()
    KEYWORD = auto()
    LITERAL = auto()
    TYPE = auto()
    IDENTIFIER = auto()
    SYMBOL = auto()
    OPERATOR = auto()
    OPEN_DELIMITER = auto()
    CLOSE_DELIMITER = auto()
    UNKNOWN = auto()
    INVALID = auto()
    EOF = auto()


# Aliases for simpler groups
class Eof(TokenKind):
    def __init__(self):
        super().__init__(TokenType.EOF)


class Comment(TokenKind):
    def __init__(self):
        super().__init__(TokenType.COMMENT)


class Whitespace(TokenKind):
    def __init__(self):
        super().__init__(TokenType.WHITESPACE)


class Type(TokenKind):
    def __init__(self):
        super().__init__(TokenType.TYPE)


class Identifier(TokenKind):
    def __init__(self):
        super().__init__(TokenType.IDENTIFIER)


class Unknown(TokenKind):
    def __init__(self):
        super().__init__(TokenType.UNKNOWN)


class Invalid(TokenKind):
    def __init__(self):
        super().__init__(TokenType.INVALID)


class Operator(TokenKind):
    def __init__(self):
        super().__init__(TokenType.OPERATOR)


class KeywordType(Enum):
    CONST = auto()
    LET = auto()
    IN = auto()
    IF = auto()
    THEN = auto
    ELSE = auto()
    WHERE = auto()
    INFIX = auto()
    INFIXR = auto()
    INFIXL = auto()


class Keyword(TokenKind):
    def __init__(self, keyword_type: KeywordType):
        super().__init__(TokenType.KEYWORD)
        self.keyword_type = keyword_type

    def __str__(self):
        return f"Keyword({self.keyword_type})"


class LiteralType(Enum):
    STRING = auto()
    NUMBER = auto()
    BOOL = auto()


class Literal(TokenKind):
    def __init__(self, literal_type: LiteralType):
        super().__init__(TokenType.LITERAL)
        self.literal_type = literal_type

    def __str__(self):
        return f"Literal({self.literal_type})"


class NumberType(Enum):
    INT = auto()
    FLOAT = auto()


class Number(Literal):
    def __init__(self, number_type: NumberType):
        super().__init__(LiteralType.NUMBER)
        self.number_type = number_type

    def __str__(self):
        return f"Number({self.number_type})"


class NumericalSuffix(Enum):
    UNSIGNED = auto()
    FLOAT = auto()


class Integer(Number):
    def __init__(self, base: int, int_value: int, suffix: NumericalSuffix = None):
        super().__init__(NumberType.INT)
        self.base = base
        self.int_value = int_value
        self.suffix = suffix

    def __str__(self):
        return f"Integer({self.int_value})"


class Float(Number):
    def __init__(self, float_value: float, suffix: NumericalSuffix = None):
        super().__init__(NumberType.FLOAT)
        self.float_value = float_value
        self.suffix = suffix

    def __str__(self):
        return f"Float({self.float_value})"


class String(Literal):
    def __init__(self, content: str):
        super().__init__(LiteralType.STRING)
        self.content = content

    def __str__(self):
        return f"String({repr(self.content)})"


class Bool(Literal):
    def __init__(self, bool_value: bool):
        super().__init__(self, LiteralType.BOOL)
        self.bool_value = bool_value

    def __str__(self):
        return f"Bool({self.bool_value})"


class DelimiterType(Enum):
    PAREN = auto()      # ()
    BRACKET = auto()    # []
    BRACE = auto()      # {}


class OpenDelimiter(TokenKind):
    def __init__(self, delimiter_type: DelimiterType):
        super().__init__(TokenType.OPEN_DELIMITER)
        self.delimiter_type = delimiter_type


class CloseDelimiter(TokenKind):
    def __init__(self, delimiter_type: DelimiterType):
        super().__init__(TokenType.CLOSE_DELIMITER)
        self.delimiter_type = delimiter_type


class SymbolType(Enum):
    COLON = auto()
    SEMICOLON = auto()
    COMMA = auto()
    DOT = auto()
    ASSIGN = auto()


class Symbol(TokenKind):
    def __init__(self, symbol_type: SymbolType):
        super().__init__(TokenType.SYMBOL)
        self.symbol_type = symbol_type
