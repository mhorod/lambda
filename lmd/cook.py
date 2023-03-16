from typing import List

from lmd import lex
from lmd.tokens import *
from lmd.errors import *


def cook_tokens(tokens: List[lex.RawToken], error_report: ErrorReport) -> List[Token]:
    cooked = []
    group_to_cooker = {
        lex.TokenGroup.WHITESPACE: cook_whitespace,
        lex.TokenGroup.COMMENT: cook_comment,
        lex.TokenGroup.LITERAL: cook_literal,
        lex.TokenGroup.NAME: cook_name,
        lex.TokenGroup.DELIMITER: cook_delimiter,
        lex.TokenGroup.OPERATOR: cook_operator,
        lex.TokenGroup.SYMBOL: cook_symbol,
        lex.TokenGroup.UNKNOWN: cook_unknown,
    }

    for token in tokens:
        cooked.append(group_to_cooker[token.group](token, error_report))

    return cooked


def make_token(raw_token: lex.RawToken, kind: TokenKind):
    return Token(raw_token.span, kind, raw_token.text)


def cook_whitespace(token: lex.RawToken, error_report: ErrorReport) -> Token:
    return make_token(token, Whitespace())


def cook_comment(token: lex.RawToken, error_report: ErrorReport) -> Token:
    return make_token(token, Comment())


def cook_literal(token: lex.RawToken, error_report: ErrorReport) -> Token:
    if token.type == lex.LiteralType.NUMBER:
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
    'const' : KeywordType.CONST,
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


def cook_name(token: lex.RawToken, error_report: ErrorReport) -> Token:
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


def cook_delimiter(token: lex.RawToken, error_report: ErrorReport) -> Token:
    Kind, delimiter_type = PARENS[token.text]
    return make_token(token, Kind(delimiter_type))


def cook_operator(token: lex.RawToken, error_report: ErrorReport) -> Token:
    return make_token(token, Operator())


def cook_symbol(token: lex.RawToken, error_report: ErrorReport) -> Token:
    return make_token(token, Symbol())


def cook_unknown(token: lex.RawToken, error_report: ErrorReport) -> Token:
    message = Message(token.span, f"Unknown token: `{token.text}`")
    error_report.add(Error(message))
    return make_token(token, Unknown())
