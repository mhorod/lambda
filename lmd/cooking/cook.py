from typing import List, Tuple

from lmd.lexing import *

from lmd.util.token import Token
from lmd.util.error import *

from lmd.cooking.tokens import *
from lmd.cooking.error import *


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
    if not token.kind.terminated:
        error_report.add(unterminated_comment(token))
    return make_token(token, Comment())


def cook_literal(token: Token, error_report: ErrorReport) -> Token:
    if token.kind.literal_type == lex.LiteralType.NUMBER:
        return cook_number(token, error_report)
    else:
        return cook_string(token, error_report)


PREFIX_TO_BASE = {
    '0x': 16,
    '0o': 8,
    '0b': 2,
}

BASE_TO_FLOAT_ERROR = {
    16: hex_float_not_supported,
    8: octal_float_not_supported,
    2: binary_float_not_supported,
}

BASE_TO_DIGITS = {
    2: '01',
    8: '01234567',
    10: '0123456789',
    16: '0123456789ABCDEFabcdef'
}

TEXT_TO_SUFFIX = {
    'u': NumericalSuffix.UNSIGNED,
    'f': NumericalSuffix.FLOAT,
    '': None,
}


def cook_number(token: Token, error_report: ErrorReport) -> Token:
    _, _, suffix = split_number(token)
    if suffix and suffix not in TEXT_TO_SUFFIX:
        error_report.add(invalid_number_suffix(token, suffix))
        return make_token(token, Invalid())

    if token.text.count('.') > 0 or is_float_suffix(suffix):
        return cook_float(token, error_report)
    else:
        return cook_integer(token, error_report)


def is_float_suffix(suffix: str) -> bool:
    return suffix == 'f'


def split_number(token: Token) -> Tuple[str, str, str]:
    if token.kind.base != 10:
        prefix = token.text[:2]
        text = token.text[2:]
    else:
        prefix = ''
        text = token.text

    digits = BASE_TO_DIGITS[token.kind.base]
    number = ''
    for c in text:
        if c == '.' or c in digits:
            number += c
        else:
            break
    suffix = text[len(number):]
    return prefix, number, suffix


def cook_float(token: Token, error_report: ErrorReport) -> Token:
    dots = token.text.count('.')
    if dots > 1:
        error_report.add(invalid_float_literal(token))
        return make_token(token, Invalid())
    elif token.kind.base != 10:
        error_report.add(BASE_TO_FLOAT_ERROR[token.kind.base](token))
        return make_token(token, Invalid())
    else:
        _, number, suffix = split_number(token)
        suffix = TEXT_TO_SUFFIX[suffix]
        return make_token(token, Float(float(number), suffix))


def cook_integer(token: Token, error_report: ErrorReport) -> Token:
    _, number, suffix = split_number(token)
    base = token.kind.base
    if not number:
        error_report.add(number_without_digits(token))
        return make_token(token, Invalid())
    else:
        suffix = TEXT_TO_SUFFIX[suffix]
        return make_token(token, Integer(base, int(number, base), suffix))


def cook_string(token: Token, error_report: ErrorReport) -> Token:
    if not token.kind.terminated:
        error_report.add(unterminated_string(token))
        content = token.text[1:]
    else:
        content = token.text[1:-1]
    content = unescape(content)
    return make_token(token, String(content))


ESCAPES = {
    '"': '"',
    'n': '\n',
    't': '\t',
    '\\': '\\',
    'r':  '\r'
}


def unescape(text: str) -> str:
    result = ''
    i = 0
    while i < len(text):
        if text[i] == '\\' and i + 1 < len(text) and text[i + 1] in ESCAPES:
            result += ESCAPES[text[i + 1]]
            i += 2
        else:
            result += text[i]
            i += 1
    return result


KEYWORDS = {
    'const': KeywordType.CONST,

    'pub': KeywordType.PUB,
    'use': KeywordType.USE,

    'if': KeywordType.IF,
    'then': KeywordType.THEN,
    'else': KeywordType.ELSE,

    'let': KeywordType.LET,
    'in': KeywordType.IN,
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
    error_report.add(unknown_token(token))
    return make_token(token, Unknown())
