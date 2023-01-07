from dataclasses import dataclass
from enum import Enum, auto

import lmd.source


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


class TokenKind:
    def __init__(self, token_type: TokenType):
        self.token_type = token_type

    def extends(self, base):
        if not isinstance(self, type(base)):
            return False
        for attr, base_value in base.kind_attrs().items():
            if getattr(self, attr) != base_value:
                return False
        return True

    def kind_attrs(self):
        '''
        Get attributes that describe the kind 
        '''
        return {
            k: self.__dict__[k]
            for k in self.__dict__.keys()
            if not k.startswith('_')
        }

    def __str__(self):
        return f"{type(self).__name__}"

# Aliases for simpler groups


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


class Operator(TokenKind):
    def __init__(self):
        super().__init__(TokenType.OPERATOR)


class KeywordType(Enum):
    LET = auto()
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


class Number(Literal):
    def __init__(self, number_value):
        super().__init__(LiteralType.NUMBER)
        self.number_value = number_value

    def __str__(self):
        return f"Number({self.number_value})"


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
        super().__init__(self, TokenType.OPEN_DELIMITER)
        self.delimiter_type = delimiter_type


class CloseDelimiter(TokenKind):
    def __init__(self, delimiter_type: DelimiterType):
        super().__init__(self, TokenType.CLOSE_DELIMITER)
        self.delimiter_type = delimiter_type


class SymbolType(Enum):
    COLON = auto()
    SEMICOLON = auto()
    COMMA = auto()
    DOT = auto()


class Symbol(TokenKind):
    def __init__(self, symbol_type: SymbolType):
        super().__init__(self, TokenType.SYMBOL)
        self.symbol_type = symbol_type


@dataclass
class Token:
    span: lmd.source.Span
    kind: TokenKind
    text: str

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        elif self.kind != other.kind:
            return False
        elif self.text != other.text:
            return False
        return True

    def __str__(self):
        return f'{self.span}: {self.kind} {repr(self.text)}'
