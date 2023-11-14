from typing import List

from lmd.util.source import *
from lmd.output.error import SimpleErrorPrinter
from lmd.util.error import ErrorReport
from lmd.lexing import lex
from lmd.cooking import cook, tokens
from lmd.parsing import parse
from lmd.modules import module_tree
from lmd.output.ast import *
from lmd.ast import expressions
from lmd.semantic_analysis import semantic_analysis


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


def build_module_tree(asts, report):
    program_module_tree = {}
    for ast in asts:
        tree = module_tree.build_module_tree(ast)
        program_module_tree = module_tree.merge_trees(
            program_module_tree, tree)
    module_tree.report_multiple_definitions(program_module_tree, report)
    return program_module_tree, asts


def transform_expressions(asts, report):
    asts = [
        expressions.transform_expressions(ast, report)
        for ast in asts
    ]
    return asts

def analyse_semantics(asts, report):
    semantic_analysis.analyse_semantics(asts, report)
    return asts

def interpret_sources(sources: List[Source]):
    pipeline = [
        lex_srcs,
        cook_tokens,
        filter_whitespace,
        parse_tokens,
        transform_expressions,
        analyse_semantics
    ]

    asts = run_pipeline(sources, pipeline)

    printer = ASTPrinter()
    for ast in asts:
        printer.visit(ast)
