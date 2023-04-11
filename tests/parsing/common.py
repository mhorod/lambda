from lmd.util.source import *
from lmd.util.token import *

from lmd.ast.nodes import *


def make_tokens(tokens):
    text = "".join([token[0] for token in tokens])
    src = Source("test", text)
    begin = 0
    result = []
    for text, kind in tokens:
        token = Token(Span(src, begin, begin + len(text)), kind, text)
        result.append(token)
        begin += len(text)
    return result


def program_node(*children):
    spans = [child.span for child in children]
    span = wrapping_span(spans)
    return ProgramNode(span, list(children))


def const_node(*children):
    spans = [child.span for child in children]
    span = wrapping_span(spans)
    _, name, _, value = children
    return ConstNode(span, name, value)


def pub_node(*children):
    spans = [child.span for child in children]
    span = wrapping_span(spans)
    return PubNode(span, children[1])
