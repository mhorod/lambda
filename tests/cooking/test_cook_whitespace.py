from .common import *


class TestCookWhitespace(CookingTestCase):
    def test_cooking_empty_list_produces_no_tokens_and_no_errors(self):
        cooked, errors = cook([])
        self.assertEqual(cooked, [])
        self.assertEqual(errors, [])

    def test_cook_whitespace(self):
        raw_tokens = [(" ", raw_token.Whitespace())]
        expected_tokens = [(" ", cooked_token.Whitespace())]
        expected_errors = []
        self.assert_cooks_to(raw_tokens, expected_tokens, expected_errors)
