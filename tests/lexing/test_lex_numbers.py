import unittest

from lmd.lexing.lex import *
from lmd.util.source import *


def make_src(s):
    return Source('test', s)


class TestLexNumbers(unittest.TestCase):
    def test_lex_number(self):
        text = '123'
        src = make_src(text)
        expected = [Token(Span(src, 0, 3), Number(10), text)]
        actual = lex_source(src)
        self.assertEqual(actual, expected)

    def test_lex_number_with_underscores(self):
        text = '1_2_3'
        src = make_src(text)
        expected = [Token(Span(src, 0, 5), Number(10), text)]
        actual = lex_source(src)
        self.assertEqual(actual, expected)

    def test_lex_number_with_leading_zeros(self):
        text = '0123'
        src = make_src(text)
        expected = [Token(Span(src, 0, 4), Number(10), text)]
        actual = lex_source(src)
        self.assertEqual(actual, expected)

    def test_lex_floating_point_number(self):
        text = '123.456'
        src = make_src(text)
        expected = [Token(Span(src, 0, len(text)), Number(10), text)]
        actual = lex_source(src)
        self.assertEqual(actual, expected)

    def test_lex_floating_point_number_with_underscores(self):
        text = '1_2_3.4_5_6'
        src = make_src(text)
        expected = [Token(Span(src, 0, len(text)), Number(10), text)]
        actual = lex_source(src)
        self.assertEqual(actual, expected)

    def test_lex_floating_point_number_with_leading_zeros(self):
        text = '0123.456'
        src = make_src(text)
        expected = [Token(Span(src, 0, len(text)), Number(10), text)]
        actual = lex_source(src)
        self.assertEqual(actual, expected)

    def test_lex_floating_point_number_with_trailing_zeros(self):
        text = '123.4560'
        src = make_src(text)
        expected = [Token(Span(src, 0, len(text)), Number(10), text)]
        actual = lex_source(src)
        self.assertEqual(actual, expected)

    def test_lex_number_with_hex_prefix(self):
        text = '0xdeadbeef'
        src = make_src(text)
        expected = [Token(Span(src, 0, len(text)), Number(16), text)]
        actual = lex_source(src)
        self.assertEqual(actual, expected)

    def test_lex_number_with_hex_prefix_and_underscores(self):
        text = '0xdead_beef'
        src = make_src(text)
        expected = [Token(Span(src, 0, len(text)), Number(16), text)]
        actual = lex_source(src)
        self.assertEqual(actual, expected)

    def test_lex_number_with_hex_prefix_and_leading_zeros(self):
        text = '0x0deadbeef'
        src = make_src(text)
        expected = [Token(Span(src, 0, len(text)), Number(16), '0x0deadbeef')]
        actual = lex_source(src)
        self.assertEqual(actual, expected)

    def test_lex_number_with_octal_prefix(self):
        text = '0o777'
        src = make_src(text)
        expected = [Token(Span(src, 0, len(text)), Number(8), '0o777')]
        actual = lex_source(src)
        self.assertEqual(actual, expected)

    def test_lex_number_with_octal_prefix_and_underscores(self):
        text = '0o777_666'
        src = make_src(text)
        expected = [Token(Span(src, 0, len(text)), Number(8), '0o777_666')]
        actual = lex_source(src)
        self.assertEqual(actual, expected)

    def test_lex_number_with_octal_prefix_and_leading_zeros(self):
        text = '0o0777'
        src = make_src(text)
        expected = [Token(Span(src, 0, len(text)), Number(8), '0o0777')]
        actual = lex_source(src)
        self.assertEqual(actual, expected)

    def test_lex_number_with_binary_prefix(self):
        text = '0b101'
        src = make_src(text)
        expected = [Token(Span(src, 0, len(text)), Number(2), '0b101')]
        actual = lex_source(src)
        self.assertEqual(actual, expected)

    def test_lex_number_with_binary_prefix_and_underscores(self):
        text = '0b101_010'
        src = make_src(text)
        expected = [Token(Span(src, 0, len(text)), Number(2), '0b101_010')]
        actual = lex_source(src)
        self.assertEqual(actual, expected)

    def test_lex_number_with_binary_prefix_and_leading_zeros(self):
        text = '0b0101'
        src = make_src(text)
        expected = [Token(Span(src, 0, len(text)), Number(2), '0b0101')]
        actual = lex_source(src)
        self.assertEqual(actual, expected)

    def test_lex_floating_point_does_not_contain_trailing_dot(self):
        text = '1.'
        src = make_src(text)
        expected = [Token(Span(src, 0, 1), Number(10), '1'),
                    Token(Span(src, 1, 2), Operator(), '.')]
        actual = lex_source(src)
        self.assertEqual(actual, expected)

    def test_number_does_not_contain_double_dot(self):
        text = '1..2'
        src = make_src(text)
        expected = [Token(Span(src, 0, 1), Number(10), '1'),
                    Token(Span(src, 1, 3), Operator(), '..'),
                    Token(Span(src, 3, 4), Number(10), '2')]
        actual = lex_source(src)
        self.assertEqual(actual, expected)

    def test_lex_number_with_multiple_dots(self):
        text = '1.2.3'
        src = make_src(text)
        expected = [Token(Span(src, 0, len(text)), Number(10), '1.2.3')]
        actual = lex_source(src)
        self.assertEqual(actual, expected)

    def test_lex_number_with_multiple_dots_and_underscores(self):
        text = '1._.2.3._4'
        src = make_src(text)
        expected = [Token(Span(src, 0, len(text)), Number(10), '1._.2.3._4')]
        actual = lex_source(src)
        self.assertEqual(actual, expected)

    def test_lex_floating_point_number_with_binary_prefix(self):
        text = '0b1.1'
        src = make_src(text)
        expected = [Token(Span(src, 0, 5), Number(2), '0b1.1')]
        actual = lex_source(src)
        self.assertEqual(actual, expected)

    def test_lex_floating_point_number_with_octal_prefix(self):
        text = '0o1.1'
        src = make_src(text)
        expected = [Token(Span(src, 0, 5), Number(8), '0o1.1')]
        actual = lex_source(src)
        self.assertEqual(actual, expected)

    def test_lex_floating_point_number_with_hex_prefix(self):
        text = '0x1.1'
        src = make_src(text)
        expected = [Token(Span(src, 0, 5), Number(16), '0x1.1')]
        actual = lex_source(src)
        self.assertEqual(actual, expected)

    def test_lex_decimal_number_with_invalid_digits(self):
        text = '123ab'
        src = make_src(text)
        expected = [Token(Span(src, 0, 5), Number(10), '123ab')]
        actual = lex_source(src)
        self.assertEqual(actual, expected)

    def test_hex_number_with_invalid_digits(self):
        text = '0x123zg'
        src = make_src(text)
        expected = [Token(Span(src, 0, 7), Number(16), '0x123zg')]
        actual = lex_source(src)
        self.assertEqual(actual, expected)

    def test_lex_octal_number_with_invalid_digits(self):
        text = '0o1238'
        src = make_src(text)
        expected = [Token(Span(src, 0, 6), Number(8), '0o1238')]
        actual = lex_source(src)
        self.assertEqual(actual, expected)

    def test_lex_binary_number_with_invalid_digits(self):
        text = '0b1012'
        src = make_src(text)
        expected = [Token(Span(src, 0, 6), Number(2), '0b1012')]
        actual = lex_source(src)
        self.assertEqual(actual, expected)

    def test_number_with_invalid_prefix(self):
        text = '0m123'
        src = make_src(text)
        expected = [Token(Span(src, 0, 5), Number(10), '0m123')]
        actual = lex_source(src)
        self.assertEqual(actual, expected)
