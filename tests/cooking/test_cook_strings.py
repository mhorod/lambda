import unittest


from .common import *


class TestCookStrings(CookingTestCase):
    def test_cook_string(self):
        raw_tokens = [('""', raw_token.String(True))]
        expected_tokens = [('""', cooked_token.String(""))]
        expected_errors = []
        self.assert_cooks_to(raw_tokens, expected_tokens, expected_errors)

    def test_cook_unterminated_string(self):
        raw_tokens = [('"', raw_token.String(False))]
        expected_tokens = [('"', cooked_token.String(""))]
        expected_errors = [(0, unterminated_string)]
        self.assert_cooks_to(raw_tokens, expected_tokens, expected_errors)

    def test_cooked_string_content_is_unescaped(self):
        text = '"\\"\\t\\n\\r\\\\"'
        escaped_content = '"\t\n\r\\'
        raw_tokens = [(text, raw_token.String(True))]
        expected_tokens = [(text, cooked_token.String(escaped_content))]
        expected_errors = []
        self.assert_cooks_to(raw_tokens, expected_tokens, expected_errors)

    def test_cooked_unterminated_string_content_is_unescaped(self):
        text = '"\\"\\t\\n\\r\\'
        escaped_content = '"\t\n\r\\'
        raw_tokens = [(text, raw_token.String(False))]
        expected_tokens = [(text, cooked_token.String(escaped_content))]
        expected_errors = [(0, unterminated_string)]
        self.assert_cooks_to(raw_tokens, expected_tokens, expected_errors)
