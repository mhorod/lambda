import sys
import pathlib
import os

from pygments import lex

from lang.lexer.lex import lex_program
from lang.parser import parse_program, Import
from lang.interpreter import run_instructions
from lang.ast import OpenScope, CloseScope
from lang.source import Source


def import_module(path, imported=None):
    # Strip extension
    if path[-4:] != '.lmd':
        path += '.lmd'

    # Ensure that modules are imported only once
    imported = imported or set()
    if path in imported:
        return []
    imported.add(path)

    try:
        program = open(f"{path}", "r").read()
    except:
        print("Cannot import name:", path)
        return []

    path = pathlib.Path(path)
    parent = path.parent

    processed = []
    lexed = lex_program(Source(str(path), program))
    if lexed.is_err():
        for error in lexed.errors:
            error.print()
        return []

    tokens = lexed.tokens
    nodes = parse_program(tokens)
    for node in nodes:
        if type(node) == Import and node.name not in imported:
            # Import relative
            node_path = os.path.join(parent, node.name)
            processed.append(OpenScope())
            processed += import_module(node_path, imported)
            processed.append(CloseScope())
        else:
            processed.append(node)

    return processed


if __name__ == '__main__':
    filename = sys.argv[1]
    nodes = import_module(filename)
    if nodes:
        run_instructions(nodes, sys.argv[2:])
