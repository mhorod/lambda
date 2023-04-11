from lmd.util.error import *
from lmd.cooking.tokens import *


def expected_statement(token):
    span = token.span
    text = f"Unexpected token: `{token.text}`, expected `use` or declaration"
    return Error(Message(span, text))


def expected_expression(token):
    span = token.span
    text = f"Unexpected token: `{token.text}`, expected expression"
    return Error(Message(span, text))


def expected_kind(token, kind):
    span = token.span
    kind_name = kind_to_name(kind)
    text = f"Unexpected token: `{token.text}`, expected {kind_name}"
    return Error(Message(span, text))


TYPE_TO_NAME = {
    TokenType.COMMENT: "comment",
    TokenType.WHITESPACE: "whitespace",
    TokenType.IDENTIFIER: "identifier",
    TokenType.TYPE: "type",
    TokenType.OPERATOR: "operator",
}

SYMBOL_TO_NAME = {
    SymbolType.COLON: ":",
    SymbolType.SEMICOLON: ";",
    SymbolType.COMMA: ",",
    SymbolType.DOT: ".",
    SymbolType.ASSIGN: "=",
}

KEYWORD_TO_NAME = {
    KeywordType.CONST: "const",

    KeywordType.PUB: "pub",
    KeywordType.USE: "use",

    KeywordType.IF: "if",
    KeywordType.THEN: "then",
    KeywordType.ELSE: "else",

    KeywordType.LET: "let",
    KeywordType.IN: "in",
    KeywordType.WHERE: "where",

    KeywordType.INFIX: "infix",
    KeywordType.INFIXR: "infixr",
    KeywordType.INFIXL: "infixl",
}


def kind_to_name(kind):
    if kind.token_type in TYPE_TO_NAME:
        return TYPE_TO_NAME[kind.token_type]
    elif kind.token_type == TokenType.SYMBOL:
        return f"`{SYMBOL_TO_NAME[kind.symbol_type]}`"
    elif kind.token_type == TokenType.KEYWORD:
        return f"`{KEYWORD_TO_NAME[kind.keyword_type]}`"
    else:
        pass
