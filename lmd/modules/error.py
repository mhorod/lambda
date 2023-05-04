from lmd.util.error import *
from lmd.ast.nodes import *


def get_name(node):
    if isinstance(node, ConstNode):
        return node.names[0].token.text
    elif isinstance(node, PubNode):
        return node.node.names[0].token.text


def multiple_definitions(nodes):
    nodes.sort(key=lambda node: (node.span.source.name, node.span.begin))
    names = [get_name(node) for node in nodes]

    reason = Message(
        nodes[0].span,
        f"Multiple definitions of `{names[0]}`")

    messages = []
    for node in nodes:
        messages.append(Message(
            node.span,
            f"Defined here"
        ))

    return Error(reason, messages)
