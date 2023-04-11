from typing import Callable, List, Tuple

from lmd.cooking.tokens import *
from lmd.util.error import *
from lmd.ast.nodes import *

from lmd.parsing.cursor import Cursor
from lmd.parsing.combinators import *
from lmd.parsing.error import *


class ParseKind(Parser):
    def __init__(self, kind: TokenKind):
        self.kind = kind

    def parse(self, cursor: Cursor, backtrack=False) -> Result:
        token = cursor.peek_one()
        if token.kind.extends(self.kind):
            cursor.take_one()
            return Result.Ok(cursor, [TokenNode(token)], [])
        elif backtrack:
            return Result.Backtracked(cursor, [], [])
        else:
            return Result.Err(cursor, [], [expected_kind(token, self.kind)])


class Fail(Parser):
    def __init__(self, token_error):
        self.token_error = token_error

    def parse(self, cursor: Cursor, backtrack=False) -> Result:
        token = cursor.peek_one()
        if backtrack:
            return Result.Backtrack(cursor, [], [])
        else:
            return Result.Err(cursor, [], [self.token_error(token)])


def parse_tokens(tokens, error_report):
    result = parse_program(Cursor(tokens))
    for error in result.errors:
        error_report.add(error)
    return result.values[0]


def parse_program(cursor: Cursor) -> Result:
    def program_parser(cursor):
        statements = []
        errors = []
        while cursor.has():
            result = parse_statement(cursor)
            statements += result.values
            errors += result.errors
            cursor = result.cursor

        return Result.Ok(cursor, statements, errors)

    result, span = parse_with_span(Do(program_parser), cursor)
    result.values = [ProgramNode(span, result.values)]
    return result


def parse_statement(cursor: Cursor) -> Result:
    parser = Do(parse_const) | Do(parse_pub) | Fail(expected_statement)
    return parser.parse(cursor)


def parse_kind(kind: TokenKind) -> Parser:
    def parser(cursor: Cursor) -> Result:
        token = cursor.peek_one()
        if token.kind.extends(kind):
            cursor.take_one()
            return Result.Ok(cursor, TokenNode(token), [])
        else:
            return Result.Err(cursor, [], [expected_kind(token, kind)])
    return parser


def parse_whitespace(cursor: Cursor) -> Result:
    return parse_kind(Whitespace())(cursor)


def parse_pub(cursor: Cursor) -> Result:
    parser = Drop(ParseKind(Keyword(KeywordType.PUB))) >> Do(parse_const)
    result, span = parse_with_span(parser, cursor)
    if result.values:
        result.values = [PubNode(span, result.values[0])]
    return result


def parse_const(cursor: Cursor) -> Result:
    parser = Drop(ParseKind(Keyword(KeywordType.CONST))) \
        >> (ParseKind(Identifier())
            + Drop(ParseKind(Symbol(SymbolType.ASSIGN)))
            + Do(parse_expression))
    result, span = parse_with_span(parser, cursor)
    if result.values:
        result.values = [ConstNode(span, *result.values)]
    return result


def parse_expression(cursor: Cursor) -> Result:
    parser = Do(parse_expression_term) \
        + Repeat(Do(parse_expression_term)) \
        + Repeat(ParseKind(Operator()) >> Do(parse_expression_term))

    result = parser.parse(cursor)
    if result.values:
        result.values = [ExpressionNode(result.values)]
    return result


def parse_parenthesised_expression(cursor: Cursor) -> Result:
    parser = Drop(ParseKind(OpenDelimiter(DelimiterType.PAREN))) >>\
        Do(parse_expression) +\
        ParseKind(CloseDelimiter(DelimiterType.PAREN))
    result, span = parse_with_span(parser, cursor)
    result.map(lambda values: ParenthesisedExpressionNode(span, *values))
    return result


def parse_expression_term(cursor: Cursor) -> Result:
    parser = (ParseKind(Identifier()) |
              ParseKind(TokenKind(TokenType.LITERAL)) |
              Do(parse_parenthesised_expression) |
              Do(parse_if_expression) |
              Fail(expected_expression)
              )

    return parser.parse(cursor)


def parse_if_expression(cursor: Cursor) -> Result:
    parser = Drop(ParseKind(Keyword(KeywordType.IF))) >>\
        Do(parse_expression) +\
        Drop(ParseKind(Keyword(KeywordType.THEN))) +\
        Do(parse_expression) +\
        Drop(ParseKind(Keyword(KeywordType.ELSE))) +\
        Do(parse_expression)
    result, span = parse_with_span(parser, cursor)
    result.map(lambda values: IfNode(span, *values))
    return result


def parse_with_span(parser: Parser, cursor: Cursor) -> Tuple[Result, Span]:
    begin = cursor.peek_one().span.begin
    source = cursor.peek_one().span.source
    result = parser.parse(cursor)
    if result.cursor.eof():
        end = result.cursor.peek_one().span.end
    else:
        end = result.cursor.peek_one().span.begin
    span = Span(source, begin, end)
    return result, span
