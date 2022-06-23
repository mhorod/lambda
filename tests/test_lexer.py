import unittest

from lang.lexer.lex import *


class TestLexIdentifier(unittest.TestCase):
    def test_lex_identifier_returns_err_if_sequence_starts_with_digit(self):
        cursor = Cursor(Source("test", "1abc"))
        result = lex_identifier(cursor)
        self.assertTrue(result.is_err())

    def test_lex_identifier_returns_ok_if_sequence_starts_with_letter(self):
        cursor = Cursor(Source("test", "abc"))
        result = lex_identifier(cursor)
        self.assertTrue(result.is_ok())
        self.assertEqual(result.tokens, [Identifier("abc")])

    def test_lex_identifier_stops_at_symbols(self):
        cursor = Cursor(Source("test", "abc;"))
        result = lex_identifier(cursor)
        self.assertTrue(result.is_ok())
        self.assertEqual(result.tokens, [Identifier("abc")])

    def test_lexed_identifier_has_correct_location(self):
        source = Source("test", "abc")
        cursor = Cursor(source)
        result = lex_identifier(cursor)
        self.assertTrue(result.is_ok())
        self.assertEqual(result.tokens[0].location, Location(source, 0, 3))

    def test_lex_identifier_returns_err_if_sequence_starts_with_symbol(self):
        cursor = Cursor(Source("test", ":abc"))
        result = lex_identifier(cursor)
        self.assertTrue(result.is_err())


class TestLexNumber(unittest.TestCase):
    def test_lex_number_returns_err_if_sequence_starts_with_symbol(self):
        cursor = Cursor(Source("test", ":123"))
        result = lex_number(cursor)
        self.assertTrue(result.is_err())

    def test_lex_number_returns_err_if_sequence_starts_with_letter(self):
        cursor = Cursor(Source("test", "abc123"))
        result = lex_number(cursor)
        self.assertTrue(result.is_err())

    def test_lex_number_returns_ok_if_sequence_starts_with_digit(self):
        cursor = Cursor(Source("test", "123"))
        result = lex_number(cursor)
        self.assertTrue(result.is_ok())
        self.assertEqual(result.tokens, [Number("123")])

    def test_lex_number_stops_at_symbols(self):
        cursor = Cursor(Source("test", "123;"))
        result = lex_number(cursor)
        self.assertTrue(result.is_ok())
        self.assertEqual(result.tokens, [Number("123")])

    def test_lexed_number_has_correct_location(self):
        source = Source("test", "123")
        cursor = Cursor(source)
        result = lex_number(cursor)
        self.assertTrue(result.is_ok())
        self.assertEqual(result.tokens[0].location, Location(source, 0, 3))


class TestLexString(unittest.TestCase):
    def test_lex_string_returns_err_if_sequence_starts_with_symbol(self):
        cursor = Cursor(Source("test", ":\"abc\""))
        result = lex_string(cursor)
        self.assertTrue(result.is_err())

    def test_lex_string_returns_err_if_sequence_starts_with_digit(self):
        cursor = Cursor(Source("test", "123\"abc\""))
        result = lex_string(cursor)
        self.assertTrue(result.is_err())

    def test_lex_string_returns_err_if_string_is_not_terminated(self):
        cursor = Cursor(Source("test", "\"abc"))
        result = lex_string(cursor)
        self.assertTrue(result.is_err())

    def test_lex_string_returns_ok_if_string_is_terminated(self):
        cursor = Cursor(Source("test", "\"abc\""))
        result = lex_string(cursor)
        self.assertTrue(result.is_ok())
        self.assertEqual(result.tokens, [String("abc")])
