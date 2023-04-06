import unittest

from lmd.lexing.lex import *
from lmd.source import *


def make_src(s):
    return Source('test', s)


class TestLexWhitespace(unittest.TestCase):
    def test_empty_string_contains_no_tokens(self):
        src = make_src('')
        self.assertEqual(lex_source(src), [])

    def test_whitespace_is_joined_together(self):
        text = ' \r\n\t'
        src = make_src(text)
        expected = [Token(Span(src, 0, 4), Whitespace(), text)]
        actual = lex_source(src)
        self.assertEqual(actual, expected)
