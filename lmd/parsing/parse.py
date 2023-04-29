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

    def __repr__(self):
        return f'ParseKind({self.kind})'


class Fail(Parser):
    def __init__(self, token_error):
        self.token_error = token_error

    def parse(self, cursor: Cursor, backtrack=False) -> Result:
        token = cursor.peek_one()
        if backtrack:
            return Result.Backtracked(cursor, [], [])
        else:
            return Result.Err(cursor, [], [self.token_error(token)])


def parse_tokens(tokens, error_report):
    result = parse_program(Cursor(tokens))
    for error in result.errors:
        error_report.add(error)
    return result.values[0]


def parse_program(cursor: Cursor) -> Result:
    def program_parser(cursor, backtrack=False):
        statements = []
        errors = []
        while cursor.has():
            result = parse_statement(cursor, backtrack)
            statements += result.values
            errors += result.errors
            cursor = result.cursor
            if result.state == ParsingState.ERR:
                break

        return Result.Ok(cursor, statements, errors)

    result, span = parse_with_span(Do(program_parser), cursor)
    result.values = [ProgramNode(span, result.values)]
    return result


def parse_statement(cursor: Cursor, backtrack=False) -> Result:
    parser = Do(parse_const) | Do(parse_pub) | Fail(expected_statement)
    return parser.parse(cursor, backtrack)


def parse_whitespace(cursor: Cursor) -> Result:
    return ParseKind(Whitespace())(cursor)


def parse_pub(cursor: Cursor, backtrack=False) -> Result:
    parser = Drop(ParseKind(Keyword(KeywordType.PUB))) >> Do(parse_const)
    result, span = parse_with_span(parser, cursor, backtrack)
    if result.values:
        result.values = [PubNode(span, result.values[0])]
    return result


def parse_const(cursor: Cursor, backtrack=False) -> Result:
    parser = Drop(ParseKind(Keyword(KeywordType.CONST))) \
        >> (Repeat1(ParseKind(Identifier())).map(lambda values: values)
            + Drop(ParseKind(Symbol(SymbolType.ASSIGN)))
            + Do(parse_expression))
    result, span = parse_with_span(parser, cursor, backtrack)
    result = result.mapped(lambda values: ConstNode(span, *values))
    return result


def parse_expression(cursor: Cursor, backtrack=False) -> Result:
    parser = Repeat1(Do(parse_expression_term)) \
        + Repeat(ParseKind(Operator()) >> Repeat1(Do(parse_expression_term)))

    result = parser.parse(cursor, backtrack)
    result.values = [value for value in result.values if value]
    result.values = [ExpressionNode(result.values)]
    return result


def parse_parenthesised_expression(cursor: Cursor, backtrack=False) -> Result:
    parser = Drop(ParseKind(OpenDelimiter(DelimiterType.PAREN))) >>\
        Do(parse_expression) +\
        Drop(ParseKind(CloseDelimiter(DelimiterType.PAREN)))
    result, span = parse_with_span(parser, cursor, backtrack=backtrack)
    return result.mapped(lambda values: ParenthesisedExpressionNode(span, *values))


def parse_expression_term(cursor: Cursor, backtrack=False) -> Result:
    parser = (Do(parse_qualified_identifier) |
              ParseKind(TokenKind(TokenType.LITERAL)) |
              Do(parse_parenthesised_expression) |
              Do(parse_if_expression) |
              Do(parse_fn_expression) |
              Fail(expected_expression)
              )
    result = parser.parse(cursor, backtrack=backtrack)
    return result


def parse_if_expression(cursor: Cursor, backtrack=False) -> Result:
    parser = Drop(ParseKind(Keyword(KeywordType.IF))) >>\
        Do(parse_expression) +\
        Drop(ParseKind(Keyword(KeywordType.THEN))) +\
        Do(parse_expression) +\
        Drop(ParseKind(Keyword(KeywordType.ELSE))) +\
        Do(parse_expression)
    result, span = parse_with_span(parser, cursor, backtrack)
    if result.values:
        result.values = [IfNode(span, *result.values)]
    return result


def parse_fn_expression(cursor: Cursor, backtrack=False) -> Result:
    parser = Drop(ParseKind(Keyword(KeywordType.FN))) >>\
        Repeat1(Do(parse_qualified_identifier)) +\
        Drop(ParseKind(Symbol(SymbolType.FAT_ARROW))) +\
        Do(parse_expression)
    result, span = parse_with_span(parser, cursor, backtrack)
    if result.values:
        result.values = [FnNode(span, *result.values)]
    return result


def parse_qualified_identifier(cursor: Cursor, backtrack=False) -> Result:
    parser = Repeat(ParseKind(Type()) + Drop(ParseKind(Symbol(SymbolType.DOT)))) +\
        ParseKind(Identifier())

    result, span = parse_with_span(parser, cursor, backtrack)
    if result.values:
        result.values = [QualifiedIdentifierNode(span, result.values)]
    return result


def parse_with_span(parser: Parser, cursor: Cursor, backtrack=False) -> Tuple[Result, Span]:
    begin = cursor.peek_one().span.begin
    source = cursor.peek_one().span.source
    result = parser.parse(cursor, backtrack=backtrack)
    if result.cursor.eof():
        end = result.cursor.peek_one().span.end
    else:
        end = result.cursor.peek_one().span.begin
    span = Span(source, begin, end)
    return result, span
