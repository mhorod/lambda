from enum import Enum, auto

import unittest

from lmd.tokens import *


class MockTokenType(Enum):
    A = auto()
    B = auto()


class MockTokenKindA(TokenKind):
    def __init__(self, value: MockTokenType):
        super().__init__(MockTokenKindA)
        self.mock_a_value = value


class MockTokenKindB(MockTokenKindA):
    def __init__(self, value: MockTokenType):
        super().__init__(MockTokenKindB)
        self.mock_b_value = value


class TestTokenKind(unittest.TestCase):
    def test_kind_extends_itself(self):
        kind = TokenKind(1)
        assert kind.extends(kind)

    def test_derived_kind_extends_itself(self):
        derived = MockTokenKindA(MockTokenType.A)
        assert derived.extends(derived)

    def test_derived_kind_extends_base(self):
        base = TokenKind(MockTokenKindA)
        derived = MockTokenKindA(MockTokenType.A)
        assert derived.extends(base)

    def test_derived_derived_kind_extends_base_and_derived(self):
        base = TokenKind(MockTokenKindA)
        derived = MockTokenKindA(MockTokenKindB)
        derived_derived = MockTokenKindB(MockTokenType.A)

        assert derived_derived.extends(base)
        assert derived_derived.extends(derived)
