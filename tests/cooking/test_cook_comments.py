from .common import *


class TestCookComments(CookingTestCase):
    def test_cook_line_comment(self):
        raw_tokens = [("-- comment", raw_token.LineComment())]
        expected_tokens = [("-- comment", cooked_token.Comment())]
        expected_errors = []
        self.assert_cooks_to(raw_tokens, expected_tokens, expected_errors)

    def test_cook_block_comment(self):
        raw_tokens = [("{- comment -}", raw_token.BlockComment(True))]
        expected_tokens = [("{- comment -}", cooked_token.Comment())]
        expected_errors = []
        self.assert_cooks_to(raw_tokens, expected_tokens, expected_errors)

    def test_cook_unterminated_block_comment(self):
        raw_tokens = [("{- comment", raw_token.BlockComment(False))]
        expected_tokens = [("{- comment", cooked_token.Comment())]
        expected_errors = [(0, unterminated_comment)]
        self.assert_cooks_to(raw_tokens, expected_tokens, expected_errors)
