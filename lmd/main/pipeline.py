from typing import List

from lmd.util.source import *
from lmd.output.error import SimpleErrorPrinter
from lmd.util.error import ErrorReport
from lmd.lexing import lex
from lmd.cooking import cook, tokens
from lmd.parsing import parse
from lmd.output.ast import *


def run_pipeline(srcs, pipeline):
    error_printer = SimpleErrorPrinter()
    report = ErrorReport()
    value = srcs
    for phase in pipeline:
        value = phase(value, report)
        if report.has_errors():
            error_printer.print_error_report(report)
            return value
    return value


def lex_srcs(srcs, _):
    return [lex.lex_source(src) for src in srcs]


def cook_tokens(srcs, report):
    return [cook.cook_tokens(src, report) for src in srcs]


def filter_whitespace(srcs, _):
    return [[token for token in cooked_tokens
            if not token.kind.extends(tokens.Comment())
            and not token.kind.extends(tokens.Whitespace())]
            for cooked_tokens in srcs]


def parse_tokens(srcs, report):
    return [parse.parse_tokens(cooked_tokens, report)
            for cooked_tokens in srcs]


def interpret_sources(sources: List[Source]):
    pipeline = [
        lex_srcs,
        cook_tokens,
        filter_whitespace,
        parse_tokens
    ]

    asts = run_pipeline(sources, pipeline)
    for ast in asts:
        ASTPrinter().visit(ast)
