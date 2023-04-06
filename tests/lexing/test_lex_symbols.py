import unittest

from lmd.lexing.lex import *
from lmd.util.source import *


def make_src(s):
    return Source('test', s)


class TestLexSymbols(unittest.TestCase):
    def test_symbols_are_not_joined_together(self):
        text = ':,;'
        src = make_src(text)
        expected = [
            Token(Span(src, 0, 1), Symbol(), ':'),
            Token(Span(src, 1, 2), Symbol(), ','),
            Token(Span(src, 2, 3), Symbol(), ';'),
        ]
        actual = lex_source(src)
        self.assertEqual(actual, expected)

    def test_delimiters_are_not_joined_together(self):
        text = '()[]{}'
        src = make_src(text)
        expected = [
            Token(Span(src, 0, 1), Delimiter(), '('),
            Token(Span(src, 1, 2), Delimiter(), ')'),
            Token(Span(src, 2, 3), Delimiter(), '['),
            Token(Span(src, 3, 4), Delimiter(), ']'),
            Token(Span(src, 4, 5), Delimiter(), '{'),
            Token(Span(src, 5, 6), Delimiter(), '}'),
        ]
        actual = lex_source(src)
        self.assertEqual(actual, expected)

    def test_delimiters_and_symbols_are_not_joined_together(self):
        text = '(,);'
        src = make_src(text)
        expected = [
            Token(Span(src, 0, 1), Delimiter(), '('),
            Token(Span(src, 1, 2), Symbol(), ','),
            Token(Span(src, 2, 3), Delimiter(), ')'),
            Token(Span(src, 3, 4), Symbol(), ';'),
        ]
        actual = lex_source(src)
        self.assertEqual(actual, expected)

    def test_operators_are_joined_together(self):
        text = '++='
        src = make_src(text)
        expected = [
            Token(Span(src, 0, 3), Operator(), '++='),
        ]
        actual = lex_source(src)
        self.assertEqual(actual, expected)

    def test_operators_do_not_include_symbols(self):
        text = ',+;+=:'
        src = make_src(text)
        expected = [
            Token(Span(src, 0, 1), Symbol(), ','),
            Token(Span(src, 1, 2), Operator(), '+'),
            Token(Span(src, 2, 3), Symbol(), ';'),
            Token(Span(src, 3, 5), Operator(), '+='),
            Token(Span(src, 5, 6), Symbol(), ':'),
        ]
        actual = lex_source(src)
        self.assertEqual(actual, expected)

    def test_operators_do_not_include_delimiters(self):
        text = '(++)'
        src = make_src(text)
        expected = [
            Token(Span(src, 0, 1), Delimiter(), '('),
            Token(Span(src, 1, 3), Operator(), '++'),
            Token(Span(src, 3, 4), Delimiter(), ')'),
        ]
        actual = lex_source(src)
        self.assertEqual(actual, expected)
