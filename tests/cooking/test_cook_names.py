from .common import *

from lmd.cooking.cook import *


class TestCookNames(CookingTestCase):
    def test_cook_bool_names(self):
        raw_tokens = [
            ('True', raw_token.Name()),
            ('False', raw_token.Name()),
        ]

        expected_tokens = [
            ('True', cooked_token.Bool(True)),
            ('False', cooked_token.Bool(False)),
        ]

        expected_errors = []
        self.assert_cooks_to(raw_tokens, expected_tokens, expected_errors)

    def test_cooking_non_capitalized_name_produces_identifier(self):
        raw_tokens = [('foo', raw_token.Name())]
        expected_tokens = [('foo', cooked_token.Identifier())]
        expected_errors = []
        self.assert_cooks_to(raw_tokens, expected_tokens, expected_errors)

    def test_cooking_name_starting_with_apostrophe_produces_identifier(self):
        raw_tokens = [('\'Foo', raw_token.Name())]
        expected_tokens = [('\'Foo', cooked_token.Identifier())]
        expected_errors = []
        self.assert_cooks_to(raw_tokens, expected_tokens, expected_errors)

    def test_cooking_name_starting_with_underscore_produces_identifier(self):
        raw_tokens = [('_Foo', raw_token.Name())]
        expected_tokens = [('_Foo', cooked_token.Identifier())]
        expected_errors = []
        self.assert_cooks_to(raw_tokens, expected_tokens, expected_errors)

    def test_cooking_capitalized_name_produces_type(self):
        raw_tokens = [('Foo', raw_token.Name())]
        expected_tokens = [('Foo', cooked_token.Type())]
        expected_errors = []
        self.assert_cooks_to(raw_tokens, expected_tokens, expected_errors)

    def test_cooking_bool_name_with_invalid_case_does_not_produce_bool(self):
        raw_tokens = [
            ('true', raw_token.Name()),
            ('TRUE', raw_token.Name()),
            ('false', raw_token.Name()),
            ('FALSE', raw_token.Name()),
        ]

        expected_tokens = [
            ('true', cooked_token.Identifier()),
            ('TRUE', cooked_token.Type()),
            ('false', cooked_token.Identifier()),
            ('FALSE', cooked_token.Type()),
        ]

        expected_errors = []
        self.assert_cooks_to(raw_tokens, expected_tokens, expected_errors)

    def test_cooking_unknown_token_produces_error(self):
        raw_tokens = [('<unk>', raw_token.Unknown())]
        expected_tokens = [('<unk>', cooked_token.Unknown())]
        expected_errors = [(0, unknown_token)]
        self.assert_cooks_to(raw_tokens, expected_tokens, expected_errors)

    def test_cook_keywords(self):
        raw_tokens = [
            ('const', raw_token.Name()),

            ('pub', raw_token.Name()),
            ('use', raw_token.Name()),

            ('if', raw_token.Name()),
            ('then', raw_token.Name()),
            ('else', raw_token.Name()),

            ('let', raw_token.Name()),
            ('in', raw_token.Name()),
            ('where', raw_token.Name()),

            ('infix', raw_token.Name()),
            ('infixr', raw_token.Name()),
            ('infixl', raw_token.Name()),
        ]

        expected_tokens = [
            ('const', cooked_token.Keyword(KeywordType.CONST)),

            ('pub', cooked_token.Keyword(KeywordType.PUB)),
            ('use', cooked_token.Keyword(KeywordType.USE)),

            ('if', cooked_token.Keyword(KeywordType.IF)),
            ('then', cooked_token.Keyword(KeywordType.THEN)),
            ('else', cooked_token.Keyword(KeywordType.ELSE)),

            ('let', cooked_token.Keyword(KeywordType.LET)),
            ('in', cooked_token.Keyword(KeywordType.IN)),
            ('where', cooked_token.Keyword(KeywordType.WHERE)),

            ('infix', cooked_token.Keyword(KeywordType.INFIX)),
            ('infixr', cooked_token.Keyword(KeywordType.INFIXR)),
            ('infixl', cooked_token.Keyword(KeywordType.INFIXL)),
        ]

        expected_errors = []
        self.assert_cooks_to(raw_tokens, expected_tokens, expected_errors)
