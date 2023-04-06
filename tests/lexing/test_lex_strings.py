import unittest

from lmd.lexing.lex import *
from lmd.source import *


def make_src(s):
    return Source('test', s)


class TestLexStrings(unittest.TestCase):
    def test_lex_empty_string(self):
        text = '""'
        src = make_src(text)
        expected = [Token(Span(src, 0, 2), String(True), '""')]
        actual = lex_source(src)
        self.assertEqual(actual, expected)

    def test_lex_non_empty_string(self):
        text = '"abc"'
        src = make_src(text)
        expected = [Token(Span(src, 0, 5), String(True), '"abc"')]
        actual = lex_source(src)
        self.assertEqual(actual, expected)

    def test_lex_string_with_whitespace(self):
        text = '"a b\tc"'
        src = make_src(text)
        expected = [Token(Span(src, 0, 7), String(True), '"a b\tc"')]
        actual = lex_source(src)
        self.assertEqual(actual, expected)

    def test_lex_string_with_newline(self):
        text = '"a\nb"'
        src = make_src(text)
        expected = [Token(Span(src, 0, 5), String(True), '"a\nb"')]
        actual = lex_source(src)
        self.assertEqual(actual, expected)

    def test_lex_string_with_escaped_quote(self):
        text = '"a\\"b"'
        src = make_src(text)
        expected = [Token(Span(src, 0, 6), String(True), '"a\\"b"')]
        actual = lex_source(src)
        self.assertEqual(actual, expected)

    def test_lex_string_with_escaped_characters(self):
        text = '"a\\nb\\tc\\\\"'
        src = make_src(text)
        expected = [Token(Span(src, 0, len(text)),
                          String(True), '"a\\nb\\tc\\\\"')]
        actual = lex_source(src)
        self.assertEqual(actual, expected)

    def test_lex_unterminated_string(self):
        text = '"abc'
        src = make_src(text)
        expected = [Token(Span(src, 0, len(text)), String(False), '"abc')]
        actual = lex_source(src)
        self.assertEqual(actual, expected)

    def test_lex_unterminated_string_with_escaped_quote(self):
        text = '"a\\"'
        src = make_src(text)
        expected = [Token(Span(src, 0, len(text)), String(False), '"a\\"')]
        actual = lex_source(src)
        self.assertEqual(actual, expected)
