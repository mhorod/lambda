from enum import Enum, auto

import unittest

from lmd.util.token import *


class MockTokenType(Enum):
    SIMPLE = auto()


class MockType(Enum):
    ONE = auto()
    TWO = auto()


class MockKind(TokenKind):
    def __init__(self, simple_type: MockType):
        super().__init__(MockTokenType.SIMPLE)
        self.simple_type = simple_type


class MockOne(MockKind):
    def __init__(self, value_one):
        super().__init__(MockType.ONE)
        self.value_one = value_one


class MockTwo(MockKind):
    def __init__(self, value_two):
        super().__init__(MockType.TWO)
        self.value_two = value_two


class TestTokens(unittest.TestCase):
    def test_kind_extends_itself(self):
        kind = MockKind(MockType.ONE)
        self.assertTrue(kind.extends(kind))

    def test_kind_extends_token_kind(self):
        kind = MockKind(MockType.ONE)
        base = TokenKind(MockTokenType.SIMPLE)
        self.assertTrue(kind.extends(base))

    def test_derived_kind_extends_base_kind(self):
        kind = MockOne(1)
        base = MockKind(MockType.ONE)
        self.assertTrue(kind.extends(base))

    def test_kind_does_not_extend_non_base_kind(self):
        kind = MockKind(MockType.ONE)
        base = MockKind(MockType.TWO)
        self.assertFalse(kind.extends(base))

    def test_kind_does_not_extend_itself_with_different_attrs(self):
        kind = MockOne(1)
        base = MockOne(2)
        self.assertFalse(kind.extends(base))
