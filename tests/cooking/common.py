import unittest

from lmd.util.error import ErrorReport
from lmd.util.source import *
from lmd.util.token import Token, TokenKind

from lmd.lexing import raw_token

from lmd.cooking import tokens as cooked_token
from lmd.cooking.cook import cook_tokens
from lmd.cooking.error import *


def cook(tokens):
    report = ErrorReport()
    cooked = cook_tokens(tokens, report)
    return cooked, report.errors


def make_tokens(raw, expected):
    src = Source("test", "")

    def make(lst):
        begin = 0
        result = []
        for text, kind in lst:
            token = Token(Span(src, begin, begin + len(text)), kind, text)
            result.append(token)
            begin += len(text)
        return result
    return make(raw), make(expected)


class CookingTestCase(unittest.TestCase):
    def assert_cooks_to(self, raw, expected_tokens, expected_errors):
        raw_tokens, expected_tokens = make_tokens(raw, expected_tokens)
        actual_tokens, actual_errors = cook(raw_tokens)
        expected_errors = [
            error(raw_tokens[i])
            for i, error in expected_errors
        ]
        self.assertEqual(actual_tokens, expected_tokens)
        self.assertEqual(actual_errors, expected_errors)
