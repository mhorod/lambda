from lang.cursor import TokenCursor
from lang.tokens import *
from lang.ast import *


class ParsingError(BaseException):
    pass


def parse_program(tokens):
    cursor = TokenCursor(tokens)
    nodes = []
    while cursor.has():
        current = cursor.peek()
        node = None
        if current.text == 'import':
            node = parse_import(cursor)
        elif current == '\n':
            cursor.skip()
        else:
            node = parse_block_instruction(cursor)

        if node is not None:
            nodes.append(node)
    return nodes


def parse_annotation(cursor):
    # TODO
    pass


def parse_let(cursor):
    cursor.skip()  # let
    args = []
    while type(cursor.peek()) == Identifier:
        args.append(cursor.consume().text)

    if cursor.peek().text != '=':
        raise ParsingError(f"Syntax error at: " + str(cursor.peek()))

    cursor.skip()  # =
    expr = parse_expression(cursor)
    cursor.skip()  # ;
    return Let(args[0], args[1:], expr)


def parse_expression(cursor):
    if cursor.peek().text == '{':
        return parse_block(cursor)

    args = []
    while cursor.has() and cursor.peek().text not in (';', ')', '}'):
        if cursor.peek().text == '(':
            cursor.skip()  # (
            args.append(parse_expression(cursor))
            cursor.skip()  # )
        else:
            args.append(parse_non_paren_expression(cursor))

    if len(args) == 0:
        return None
    elif len(args) == 1:
        return Expression(args[0])
    else:
        return Call(args[0], [Expression(arg) for arg in args[1:]])


def parse_block(cursor):
    cursor.skip()  # {

    args = []
    while cursor.has() and cursor.peek().text != '}':
        args.append(parse_block_instruction(cursor))

    cursor.skip()  # }
    return Block(args)


def parse_block_instruction(cursor):
    if cursor.peek().text == 'let':
        return parse_let(cursor)
    else:
        expr = parse_expression(cursor)
        if cursor.peek().text == ';':
            cursor.skip()
        return expr


def parse_non_paren_expression(cursor):
    if cursor.peek() == Identifier('if'):
        return parse_if(cursor)
    elif cursor.peek() == Identifier('fn'):
        return parse_fn(cursor)
    elif type(cursor.peek()) in (Number, String):
        return cursor.consume()
    else:
        return cursor.consume().text


def parse_if(cursor):
    cursor.skip()  # if
    condition = parse_expression(cursor)
    cursor.skip(2)  # ;then
    true_expr = parse_expression(cursor)
    cursor.skip(2)  # ;else
    false_expr = parse_expression(cursor)
    return If(condition, true_expr, false_expr)


def parse_fn(cursor):
    args = []
    cursor.skip()  # fn
    while cursor.peek().text != '=>':
        args.append(parse_identifier(cursor).text)
    cursor.skip()  # =>
    expr = parse_expression(cursor)
    return Fn(args, expr)


def parse_identifier(cursor):
    if type(cursor.peek()) != Identifier:
        raise ParsingError("Expected identifier")
    else:
        return cursor.consume()


def parse_import(cursor):
    cursor.skip()  # import
    name = cursor.consume().text
    return Import(name)
