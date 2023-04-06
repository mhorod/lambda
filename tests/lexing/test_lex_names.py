import unittest

from lmd.lexing.lex import *
from lmd.source import *


def make_src(s):
    return Source('test', s)


class TestLexNames(unittest.TestCase):
    def name_can_contain_lowercase_letters(self):
        src = make_src('abc')
        expected = [Token(Span(src, 0, 3), Name(), 'abc')]
        actual = lex_source(src)
        self.assertEqual(actual, expected)

    def test_name_can_contain_uppercase_letters(self):
        src = make_src('ABC')
        expected = [Token(Span(src, 0, 3), Name(), 'ABC')]
        actual = lex_source(src)
        self.assertEqual(actual, expected)

    def test_name_can_contain_underscores(self):
        src = make_src('a_b_c')
        expected = [Token(Span(src, 0, 5), Name(), 'a_b_c')]
        actual = lex_source(src)
        self.assertEqual(actual, expected)

    def test_name_can_contain_digits(self):
        src = make_src('a1b2c3')
        expected = [Token(Span(src, 0, 6), Name(), 'a1b2c3')]
        actual = lex_source(src)
        self.assertEqual(actual, expected)

    def test_name_can_contain_apostrophes(self):
        src = make_src("a'b'c")
        expected = [Token(Span(src, 0, 5), Name(), "a'b'c")]
        actual = lex_source(src)
        self.assertEqual(actual, expected)

    def test_name_does_not_start_with_digit(self):
        src = make_src('1abc')
        unexpected = [Token(Span(src, 1, 4), Name(), '1abc')]
        actual = lex_source(src)
        self.assertNotEqual(actual, unexpected)

    def test_name_can_start_with_underscore(self):
        src = make_src('_abc')
        expected = [Token(Span(src, 0, 4), Name(), '_abc')]
        actual = lex_source(src)
        self.assertEqual(actual, expected)

    def test_name_can_start_with_apostrophe(self):
        src = make_src("'abc")
        expected = [Token(Span(src, 0, 4), Name(), "'abc")]
        actual = lex_source(src)
        self.assertEqual(actual, expected)

    def test_name_does_not_contain_symbols(self):
        src = make_src('a,b')
        expected = [Token(Span(src, 0, 1), Name(), 'a'),
                    Token(Span(src, 1, 2), Symbol(), ','),
                    Token(Span(src, 2, 3), Name(), 'b')]
        actual = lex_source(src)
        self.assertEqual(actual, expected)

    def test_name_does_not_contain_delimiters(self):
        src = make_src('a(b')
        expected = [Token(Span(src, 0, 1), Name(), 'a'),
                    Token(Span(src, 1, 2), Delimiter(), '('),
                    Token(Span(src, 2, 3), Name(), 'b')]
        actual = lex_source(src)
        self.assertEqual(actual, expected)

    def test_name_does_not_contain_operators(self):
        src = make_src('a+b')
        expected = [Token(Span(src, 0, 1), Name(), 'a'),
                    Token(Span(src, 1, 2), Operator(), '+'),
                    Token(Span(src, 2, 3), Name(), 'b')]
        actual = lex_source(src)
        self.assertEqual(actual, expected)
