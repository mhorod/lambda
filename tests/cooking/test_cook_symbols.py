from lmd.cooking.cook import *

from .common import *


class TestCookSymbols(CookingTestCase):
    def test_cook_symbols(self):
        raw_tokens = [
            (':', raw_token.Symbol()),
            (';', raw_token.Symbol()),
            (',', raw_token.Symbol()),
            ('.', raw_token.Symbol()),
            ('=', raw_token.Symbol()),
        ]

        expected_tokens = [
            (':', cooked_token.Symbol(SymbolType.COLON)),
            (';', cooked_token.Symbol(SymbolType.SEMICOLON)),
            (',', cooked_token.Symbol(SymbolType.COMMA)),
            ('.', cooked_token.Symbol(SymbolType.DOT)),
            ('=', cooked_token.Symbol(SymbolType.ASSIGN)),
        ]

        expected_errors = []

        self.assert_cooks_to(raw_tokens, expected_tokens, expected_errors)

    def test_cook_delimiters(self):
        raw_tokens = [
            ('(', raw_token.Delimiter()),
            (')', raw_token.Delimiter()),
            ('[', raw_token.Delimiter()),
            (']', raw_token.Delimiter()),
            ('{', raw_token.Delimiter()),
            ('}', raw_token.Delimiter()),
        ]

        expected_tokens = [
            ('(', OpenDelimiter(DelimiterType.PAREN)),
            (')', CloseDelimiter(DelimiterType.PAREN)),
            ('[', OpenDelimiter(DelimiterType.BRACKET)),
            (']', CloseDelimiter(DelimiterType.BRACKET)),
            ('{', OpenDelimiter(DelimiterType.BRACE)),
            ('}', CloseDelimiter(DelimiterType.BRACE)),
        ]

        expected_errors = []
        self.assert_cooks_to(raw_tokens, expected_tokens, expected_errors)

    def test_cooking_unknon_symbol_produces_operator(self):
        raw_tokens = [
            ('+', raw_token.Symbol()),
            ('..', raw_token.Symbol()),
        ]

        expected_tokens = [
            ('+', cooked_token.Operator()),
            ('..', cooked_token.Operator()),
        ]

        expected_errors = []
        self.assert_cooks_to(raw_tokens, expected_tokens, expected_errors)
