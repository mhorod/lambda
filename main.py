import sys
import pathlib
import os

from lang.lexer import lex_program
from lang.parser import parse_program, Import
from lang.interpreter import run_instructions
from lang.ast import OpenScope, CloseScope


def import_module(path, imported=None):
    # Strip extension
    if path[-4:] == '.lmd':
        path = path[:-4]

    # Ensure that modules are imported only once
    imported = imported or set()
    if path in imported: return []
    imported.add(path)

    try:
        program = open(f"{path}.lmd", "r").read()
    except:
        print("Cannot import name:", path)
        return []

    path = pathlib.Path(path)
    parent = path.parent

    processed = []
    nodes = parse_program(lex_program(program))
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
