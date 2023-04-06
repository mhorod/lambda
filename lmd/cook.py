from typing import List

from lmd.lexing import *
from lmd.tokens import *
from lmd.errors import *


def cook_tokens(tokens: List[Token], error_report: ErrorReport) -> List[Token]:
    cooked = []
    kind_to_cooker = [
        (raw_token.Whitespace(), cook_whitespace),
        (raw_token.TokenKind(raw_token.RawTokenType.COMMENT), cook_comment),
        (raw_token.TokenKind(raw_token.RawTokenType.LITERAL), cook_literal),
        (raw_token.Name(), cook_name),
        (raw_token.Delimiter(), cook_delimiter),
        (raw_token.Operator(), cook_operator_or_symbol),
        (raw_token.Symbol(), cook_operator_or_symbol),
        (raw_token.Unknown(), cook_unknown),
    ]

    for token in tokens:
        for kind, cooker in kind_to_cooker:
            if token.kind.extends(kind):
                cooked.append(cooker(token, error_report))
                break
    return cooked


def make_token(raw_token: Token, new_kind: TokenKind):
    return Token(raw_token.span, new_kind, raw_token.text)


def cook_whitespace(token: Token, error_report: ErrorReport) -> Token:
    return make_token(token, Whitespace())


def cook_comment(token: Token, error_report: ErrorReport) -> Token:
    return make_token(token, Comment())


def cook_literal(token: Token, error_report: ErrorReport) -> Token:
    if token.kind.literal_type == lex.LiteralType.NUMBER:
        return make_token(token, Number(int(token.text)))
    else:
        if not token.terminated:
            message = Message(token.span, f"Unterminated string")
            error_report.add(Error(message))
            content = token.text[1:]
        else:
            content = token.text[1:-1]
        return make_token(token, String(content))


KEYWORDS = {
    'const': KeywordType.CONST,
    'let': KeywordType.LET,
    'in': KeywordType.IN,
    'if': KeywordType.IF,
    'then': KeywordType.THEN,
    'else': KeywordType.ELSE,
    'where': KeywordType.WHERE,
    'infix': KeywordType.INFIX,
    'infixr': KeywordType.INFIXR,
    'infixl': KeywordType.INFIXL,
}

BOOLS = {
    'True': True,
    'False': False,
}


def cook_name(token: Token, error_report: ErrorReport) -> Token:
    if token.text in KEYWORDS:
        return make_token(token, Keyword(KEYWORDS[token.text]))
    elif token.text in BOOLS:
        return make_token(token, Bool(BOOLS[token.text]))
    elif token.text[0].isupper():
        return make_token(token, Type())
    else:
        return make_token(token, Identifier())


PARENS = {
    '(': (OpenDelimiter, DelimiterType.PAREN),
    ')': (CloseDelimiter, DelimiterType.PAREN),
    '[': (OpenDelimiter, DelimiterType.BRACKET),
    ']': (CloseDelimiter, DelimiterType.BRACKET),
    '{': (OpenDelimiter, DelimiterType.BRACE),
    '}': (CloseDelimiter, DelimiterType.BRACE),
}


def cook_delimiter(token: Token, error_report: ErrorReport) -> Token:
    Kind, delimiter_type = PARENS[token.text]
    return make_token(token, Kind(delimiter_type))


SYMBOLS = {
    ':': SymbolType.COLON,
    ';': SymbolType.SEMICOLON,
    ',': SymbolType.COMMA,
    '.': SymbolType.DOT,
    '=': SymbolType.ASSIGN,
}


def cook_operator_or_symbol(token: Token, error_report: ErrorReport) -> Token:
    if token.text in SYMBOLS:
        return make_token(token, Symbol(SYMBOLS[token.text]))
    else:
        return make_token(token, Operator())


def cook_unknown(token: Token, error_report: ErrorReport) -> Token:
    message = Message(token.span, f"Unknown token: `{token.text}`")
    error_report.add(Error(message))
    return make_token(token, Unknown())
