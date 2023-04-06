from typing import Callable, List, Tuple

from lmd.cooking.tokens import *
from lmd.util.error import *
from lmd.ast.nodes import *


class Result:
    def __init__(self, cursor, value, errors, ok):
        self.cursor = cursor
        self.value = value
        self.errors = errors
        self.ok = ok
        self.commited = False

    def commit(self):
        self.commited = True

    def Ok(cursor, value, errors):
        return Result(cursor, value, errors, True)

    def Err(cursor, value, errors):
        return Result(cursor, value, errors, False)

    def merge(self, other, f):
        result = Result(
            other.cursor,
            f(self.value, other.value),
            self.errors + other.errors,
            self.ok and other.ok
        )
        result.commited = self.commited or other.commited
        return result


class Cursor:
    def __init__(self, tokens: List[Token], index: int = 0):
        self.tokens = tokens
        self.index = index
        self.consumed_begin = index

    def clone(self) -> "Cursor":
        return Cursor(self.tokens, self.index)

    def has(self, cnt: int = 1) -> bool:
        return self.index + cnt <= len(self.tokens)

    def peek_one(self) -> Token:
        if not self.has():
            return self.eof()
        else:
            return self.tokens[self.index]

    def eof(self) -> bool:
        return Token(self.tokens[-1].span, Eof(), "<eof>")

    def peek(self, cnt: int = 1) -> List[Token]:
        return self.tokens[self.index:self.index + cnt]

    def take_one(self) -> Token:
        result = self.peek_one()
        self.index += 1
        return result

    def take(self, cnt: int = 1) -> List[Token]:
        result = self.peek(cnt)
        self.index += cnt
        return result


Parser = Callable[[Cursor], Result]


class Sequential:

    @dataclass
    class Item:
        parser: Parser
        drop: bool

    @dataclass
    class Map:
        f: Callable

    def __init__(self):
        self.parsers: List[Parser] = []

    def then(self, parser: Parser):
        self.parsers.append(Sequential.Item(parser, False))
        return self

    def expect(self, parser: Parser):
        self.parsers.append(Sequential.Item(parser, True))
        return self

    def drop(self):
        self.parsers[-1].drop = True
        return self

    def map(self, f):
        self.parsers.append(Sequential.Map(f))
        return self

    def __call__(self, cursor: Cursor) -> Result:
        result = Result.Ok(cursor, [], [])
        for item in self.parsers:
            if isinstance(item, Sequential.Map):
                result.value = item.f(result.value)
            else:
                if not result.ok:
                    # If parsing failed previously just add None to the result
                    # unless the item is marked as drop
                    if not item.drop:
                        result.value.append(None)
                else:
                    # Otherwise parse the item and update the result
                    parsed = item.parser(result.cursor)
                    result.ok = result.ok and parsed.ok
                    if not item.drop:
                        result.value.append(parsed.value)
                    result.errors.extend(parsed.errors)
                    result.cursor = parsed.cursor
                    result.commited = result.commited or parsed.commited
        return result


def maybe(parser: Parser) -> Parser:
    def result(cursor: Cursor) -> Result:
        parsed = parser(cursor.clone())
        if parsed.ok:
            return parsed
        elif parsed.commited:
            return parsed
        else:
            return Result.Ok(cursor, None, [])
    return result


def repeat(parser: Parser) -> Parser:
    def result(cursor: Cursor) -> Result:
        r = Result.Ok(cursor, [], [])
        while True:
            parsed = parser(r.cursor.clone())
            if parsed.ok or parsed.commited:
                r.value.append(parsed.value)
                r.errors.extend(parsed.errors)
                r.commited = r.commited or parsed.commited
                r.cursor = parsed.cursor
                r.ok = r.ok and parsed.ok
            if not parsed.ok:
                break
        return r
    return result


def commit(parser: Parser) -> Parser:
    def result(cursor: Cursor) -> Result:
        parsed = parser(cursor.clone())
        if parsed.ok:
            parsed.commit()
            return parsed
        else:
            return parsed
    return result


def uncommit(parser: Parser) -> Parser:
    def result(cursor: Cursor) -> Result:
        parsed = parser(cursor.clone())
        parsed.commited = False
        return parsed
    return result


def parse_kind(kind: TokenKind) -> Parser:
    def parser(cursor: Cursor) -> Result:
        token = cursor.peek_one()
        if token.kind.extends(kind):
            cursor.take_one()
            return Result.Ok(cursor, TokenNode(token), [])
        else:
            message = Message(
                token.span, f"unexpected token: `{token.text}`, expected {kind}")
            return Result.Err(cursor, None, [Error(message)])
    return parser


def flatten(xs: List[List]) -> List:
    result = []
    for x in xs:
        if isinstance(x, list):
            result.extend(flatten(x))
        else:
            result.append(x)
    return result


def remove_none(xs: List) -> List:
    return [x for x in xs if x is not None]


def parse_tokens(tokens, error_report):
    result = parse_program(Cursor(tokens))
    for error in result.errors:
        error_report.add(error)
    return result.value


def parse_program(cursor: Cursor) -> Result:
    def program_parser(cursor: Cursor):
        result = Result.Ok(cursor, [], [])
        while result.cursor.has() and result.ok:
            parsed = parse_statement(result.cursor.clone())
            result = result.merge(parsed, lambda x, y: x + [y])
        return result
    result, span = parse_with_span(program_parser, cursor)
    result.value = ProgramNode(span, remove_none(flatten(result.value)))
    return result


def parse_statement(cursor: Cursor) -> Result:
    token = cursor.peek_one()
    if token.kind.extends(Keyword(KeywordType.CONST)):
        return parse_const(cursor)
    elif token.kind.extends(Keyword(KeywordType.LET)):
        return parse_let(cursor)
    else:
        message = Message(
            token.span, f"unexpected token: `{token.text}`, expected `let` or `const`")
        return Result.Err(cursor, None, [Error(message)])


def parse_whitespace(cursor: Cursor) -> Result:
    return parse_kind(Whitespace())(cursor)


def parse_const(cursor: Cursor) -> Result:
    parser = Sequential()\
        .then(commit(parse_kind(Keyword(KeywordType.CONST)))).drop() \
        .then(parse_kind(Identifier())) \
        .then(parse_kind(Symbol(SymbolType.ASSIGN))).drop() \
        .then(parse_expression)
    result, span = parse_with_span(parser, cursor)
    result.value = ConstNode(span, *result.value)
    return result


def parse_let(cursor: Cursor) -> Result:
    parser = Sequential()\
        .then(commit(parse_kind(Keyword(KeywordType.LET)))).drop() \
        .then(parse_kind(Identifier())) \
        .then(parse_kind(Symbol(SymbolType.ASSIGN))).drop() \
        .then(parse_expression) \
        .then(parse_kind(Keyword(KeywordType.IN))).drop() \
        .then(parse_expression)

    result, span = parse_with_span(parser, cursor)
    result.value = LetNode(span, *result.value)
    return result


def parse_expression(cursor: Cursor) -> Result:
    parser = Sequential() \
        .then(parse_expression_term) \
        .then(uncommit(repeat(parse_expression_term))) \
        .then(uncommit(
            repeat(
                Sequential()
                .then(commit(parse_kind(Operator())))
                .then(repeat(parse_expression_term))
            )))\
        .map(flatten)\
        .map(remove_none)

    result = parser(cursor)
    if result.value:
        result.value = ExpressionNode(result.value)
    else:
        result.value = None
    return result


def parse_parenthesised_expression(cursor: Cursor) -> Result:
    parser = Sequential()\
        .then(commit(parse_kind(OpenDelimiter(DelimiterType.PAREN)))).drop() \
        .then(parse_expression) \
        .then(parse_kind(CloseDelimiter(DelimiterType.PAREN))).drop()
    result, span = parse_with_span(parser, cursor)
    result.value = ParenthesisedExpressionNode(span, *result.value)
    return result


def parse_expression_term(cursor: Cursor) -> Result:
    token = cursor.peek_one()
    if token.kind.extends(Identifier()):
        cursor.take_one()
        return Result.Ok(cursor, TokenNode(token), [])
    elif token.kind.extends(TokenKind(TokenType.LITERAL)):
        cursor.take_one()
        return Result.Ok(cursor, TokenNode(token), [])
    elif token.kind.extends(OpenDelimiter(DelimiterType.PAREN)):
        return parse_parenthesised_expression(cursor)
    elif token.kind.extends(Keyword(KeywordType.IF)):
        return parse_if_expression(cursor)
    else:
        message = Message(
            token.span, f"unexpected token: `{token.text}`, expected expression")
        return Result.Err(cursor, None, [Error(message)])


def parse_if_expression(cursor: Cursor) -> Result:
    parser = Sequential()\
        .then(commit(parse_kind(Keyword(KeywordType.IF)))).drop() \
        .then(parse_expression) \
        .then(parse_kind(Keyword(KeywordType.THEN))).drop() \
        .then(parse_expression) \
        .then(parse_kind(Keyword(KeywordType.ELSE))).drop() \
        .then(parse_expression)
    result, span = parse_with_span(parser, cursor)
    result.value = IfNode(span, *result.value)
    return result


def parse_with_span(parser: Parser, cursor: Cursor) -> Tuple[Result, Span]:
    begin = cursor.peek_one().span.begin
    source = cursor.peek_one().span.source
    result = parser(cursor)
    if result.cursor.eof():
        end = result.cursor.peek_one().span.end
    else:
        end = result.cursor.peek_one().span.begin
    span = Span(source, begin, end)
    return result, span
