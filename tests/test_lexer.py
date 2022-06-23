
from lang.lexer.cursor import *
from lang.lexer.lex import *
import unittest


class TestCursor(unittest.TestCase):
    def dummy_source(self):
        return Source("test", "abcdefghijklmnopqrstuvwxyz")

    def test_peek_does_not_advance(self):
        cursor = Cursor(self.dummy_source())
        cursor.peek()
        self.assertEqual(cursor.take(), "a")

    def test_take_advances(self):
        cursor = Cursor(self.dummy_source())
        cursor.take()
        self.assertEqual(cursor.peek(), "b")

    def test_take_advances_by_count(self):
        cursor = Cursor(self.dummy_source())
        cursor.take(3)
        self.assertEqual(cursor.peek(), "d")

    def cursor_continues_from_current_index(self):
        cursor = Cursor(self.dummy_source())
        cursor.take(3)
        cursor.take(3)
        self.assertEqual(cursor.peek(), "g")

    def test_take_while_stops_at_first_non_matching_character(self):
        cursor = Cursor(self.dummy_source())
        taken = cursor.take_while(lambda c: c != 'c')
        self.assertEqual(cursor.peek(), 'c')
        self.assertEqual(taken, "ab")

    def test_clone_continues_from_current_index(self):
        cursor = Cursor(self.dummy_source())
        cursor.take(3)
        clone = cursor.clone()
        self.assertEqual(clone.peek(), "d")

    def test_advancing_clone_does_not_change_original(self):
        cursor = Cursor(self.dummy_source())
        clone = cursor.clone()
        clone.advance()
        self.assertEqual(cursor.peek(), "a")

    def test_take_while_does_not_exceed_limit(self):
        cursor = Cursor(self.dummy_source())
        taken = cursor.take_while(lambda c: c != 'e', limit=2)
        self.assertEqual(taken, "ab")

    def test_peek_while_does_not_consume_characters(self):
        cursor = Cursor(self.dummy_source())
        taken = cursor.peek_while(lambda c: c != 'c')
        self.assertEqual(taken, "ab")
        self.assertEqual(cursor.peek(), 'a')


class TestCursorUtils(unittest.TestCase):
    def dummy_source(self):
        return Source("test", "abcdefghijklmnopqrstuvwxyz")

    def test_take_returns_error_if_cursor_is_at_end(self):
        cursor = Cursor(self.dummy_source())
        cursor.advance(len(cursor.source.text))
        result = Ok(cursor, []).and_then(take(1))
        self.assertEqual(result.is_err(), True)

    def test_take_returns_ok_if_cursor_has_enough_characters(self):
        cursor = Cursor(self.dummy_source())
        result = Ok(cursor, []).and_then(take(1))
        self.assertEqual(result.is_err(), False)
        self.assertEqual(result.tokens, ["a"])

    def test_expect_and_skip_returns_error_if_cursor_is_at_end(self):
        cursor = Cursor(self.dummy_source())
        cursor.advance(len(cursor.source.text))
        result = Ok(cursor, []).and_then(expect_and_skip("a"))
        self.assertEqual(result.is_err(), True)

    def test_expect_and_skip_returns_error_if_cursor_has_wrong_characters(self):
        cursor = Cursor(self.dummy_source())
        result = Ok(cursor, []).and_then(expect_and_skip("bc"))
        self.assertEqual(result.is_err(), True)

    def test_expect_and_skip_returns_ok_with_empty_list_if_cursor_has_correct_characters(self):
        cursor = Cursor(self.dummy_source())
        result = Ok(cursor, []).and_then(expect_and_skip("abc"))
        self.assertEqual(result.is_err(), False)
        self.assertEqual(result.tokens, [])

    def test_peek_while_returns_ok(self):
        cursor = Cursor(self.dummy_source())
        result = Ok(cursor, []).and_then(peek_while(lambda c: c != 'c'))
        self.assertEqual(result.is_err(), False)
        self.assertEqual(result.tokens, ["ab"])

    def test_peek_while_returns_list_with_empty_string_if_cursor_is_at_end(self):
        cursor = Cursor(self.dummy_source())
        cursor.advance(len(cursor.source.text))
        result = Ok(cursor, []).and_then(peek_while(lambda c: c != 'c'))
        self.assertEqual(result.is_err(), False)
        self.assertEqual(result.tokens, [''])

    def test_peek_while_does_not_consume_characters(self):
        cursor = Cursor(self.dummy_source())
        Ok(cursor, []).and_then(peek_while(lambda c: c != 'c'))
        taken = cursor.take_while(lambda c: c != 'c')
        self.assertEqual(taken, "ab")


if __name__ == '__main__':
    print("Testing lexer")
    unittest.main()
