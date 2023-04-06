import unittest

from lmd.lexing.lex import *
from lmd.util.source import *


def make_src(s):
    return Source('test', s)


class TestLexComments(unittest.TestCase):
    def test_lex_line_comment(self):
        text = '-- this is a comment'
        src = make_src(text)
        expected = [Token(Span(src, 0, len(text)), LineComment(), text)]
        actual = lex_source(src)
        self.assertEqual(actual, expected)

    def test_lex_nested_line_comment(self):
        text = '-- this is a -- nested comment'
        src = make_src(text)
        expected = [Token(Span(src, 0, len(text)), LineComment(), text)]
        actual = lex_source(src)
        self.assertEqual(actual, expected)

    def test_lex_block_comment(self):
        text = '{- this is a comment -}'
        src = make_src(text)
        expected = [Token(Span(src, 0, len(text)), BlockComment(True), text)]
        actual = lex_source(src)
        self.assertEqual(actual, expected)

    def test_lex_block_comment_with_nested_block_comment(self):
        text = '{- this is a {- nested -} comment -}'
        src = make_src(text)
        expected = [Token(Span(src, 0, len(text)), BlockComment(True), text)]
        actual = lex_source(src)
        self.assertEqual(actual, expected)

    def test_lex_block_comment_with_nested_line_comment(self):
        text = '{- this is a -- nested comment -}'
        src = make_src(text)
        expected = [Token(Span(src, 0, len(text)), BlockComment(True), text)]
        actual = lex_source(src)
        self.assertEqual(actual, expected)

    def test_lex_unterminated_block_comment(self):
        text = '{- this is a comment'
        src = make_src(text)
        expected = [Token(Span(src, 0, len(text)), BlockComment(False), text)]
        actual = lex_source(src)
        self.assertEqual(actual, expected)

    def test_lex_unterminated_nested_block_comment(self):
        text = '{- this is a {- nested comment'
        src = make_src(text)
        expected = [Token(Span(src, 0, len(text)), BlockComment(False), text)]
        actual = lex_source(src)
        self.assertEqual(actual, expected)
