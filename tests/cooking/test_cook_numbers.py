from .common import *


class TestCookNumbers(CookingTestCase):
    def test_cook_decimal_integer(self):
        raw_tokens = [("0", raw_token.Number(10))]
        expected_tokens = [("0", cooked_token.Integer(10, 0))]
        expected_errors = []
        self.assert_cooks_to(raw_tokens, expected_tokens, expected_errors)

    def test_cook_decimal_integer_with_leading_zeroes(self):
        raw_tokens = [("001", raw_token.Number(10))]
        expected_tokens = [("001", cooked_token.Integer(10, 1))]
        expected_errors = []
        self.assert_cooks_to(raw_tokens, expected_tokens, expected_errors)

    def test_cook_decimal_integer_with_unsigned_suffix(self):
        raw_tokens = [("123u", raw_token.Number(10))]
        suffix = cooked_token.NumericalSuffix.UNSIGNED
        expected_tokens = [("123u", cooked_token.Integer(10, 123, suffix))]
        expected_errors = []
        self.assert_cooks_to(raw_tokens, expected_tokens, expected_errors)

    def test_cook_hex_integer(self):
        raw_tokens = [("0xa", raw_token.Number(16))]
        expected_tokens = [("0xa", cooked_token.Integer(16, 10))]
        expected_errors = []
        self.assert_cooks_to(raw_tokens, expected_tokens, expected_errors)

    def test_cook_hex_integer_with_leading_zeroes(self):
        raw_tokens = [("0x00f", raw_token.Number(16))]
        expected_tokens = [("0x00f", cooked_token.Integer(16, 15))]
        expected_errors = []
        self.assert_cooks_to(raw_tokens, expected_tokens, expected_errors)

    def test_cook_hex_integer_with_unsigned_suffix(self):
        raw_tokens = [("0xau", raw_token.Number(16))]
        suffix = cooked_token.NumericalSuffix.UNSIGNED
        expected_tokens = [("0xau", cooked_token.Integer(16, 10, suffix))]
        expected_errors = []
        self.assert_cooks_to(raw_tokens, expected_tokens, expected_errors)

    def test_cook_octal_integer(self):
        raw_tokens = [("0o17", raw_token.Number(8))]
        expected_tokens = [("0o17", cooked_token.Integer(8, 15))]
        expected_errors = []
        self.assert_cooks_to(raw_tokens, expected_tokens, expected_errors)

    def test_cook_octal_integer_with_leading_zeroes(self):
        raw_tokens = [("0o017", raw_token.Number(8))]
        expected_tokens = [("0o017", cooked_token.Integer(8, 15))]
        expected_errors = []
        self.assert_cooks_to(raw_tokens, expected_tokens, expected_errors)

    def test_cook_octal_integer_with_unsigned_suffix(self):
        raw_tokens = [("0o17u", raw_token.Number(8))]
        suffix = cooked_token.NumericalSuffix.UNSIGNED
        expected_tokens = [("0o17u", cooked_token.Integer(8, 15, suffix))]
        expected_errors = []
        self.assert_cooks_to(raw_tokens, expected_tokens, expected_errors)

    def test_cook_binary_integer(self):
        raw_tokens = [("0b101", raw_token.Number(2))]
        expected_tokens = [("0b101", cooked_token.Integer(2, 5))]
        expected_errors = []
        self.assert_cooks_to(raw_tokens, expected_tokens, expected_errors)

    def test_cook_binary_integer_with_leading_zeroes(self):
        raw_tokens = [("0b00101", raw_token.Number(2))]
        expected_tokens = [("0b00101", cooked_token.Integer(2, 5))]
        expected_errors = []
        self.assert_cooks_to(raw_tokens, expected_tokens, expected_errors)

    def test_cook_binary_integer_with_unsigned_suffix(self):
        raw_tokens = [("0b101u", raw_token.Number(2))]
        suffix = cooked_token.NumericalSuffix.UNSIGNED
        expected_tokens = [("0b101u", cooked_token.Integer(2, 5, suffix))]
        expected_errors = []
        self.assert_cooks_to(raw_tokens, expected_tokens, expected_errors)

    def test_cook_float(self):
        raw_tokens = [("1.5", raw_token.Number(10))]
        expected_tokens = [("1.5", cooked_token.Float(1.5))]
        expected_errors = []
        self.assert_cooks_to(raw_tokens, expected_tokens, expected_errors)

    def test_cook_float_with_leading_zeroes(self):
        raw_tokens = [("001.0", raw_token.Number(10))]
        expected_tokens = [("001.0", cooked_token.Float(1.0))]
        expected_errors = []
        self.assert_cooks_to(raw_tokens, expected_tokens, expected_errors)

    def test_cook_float_with_trailing_zeroes(self):
        raw_tokens = [("1.290", raw_token.Number(10))]
        expected_tokens = [("1.290", cooked_token.Float(1.29))]
        expected_errors = []
        self.assert_cooks_to(raw_tokens, expected_tokens, expected_errors)

    def test_cook_float_with_suffix(self):
        raw_tokens = [("15f", raw_token.Number(10))]
        suffix = cooked_token.NumericalSuffix.FLOAT
        expected_tokens = [("15f", cooked_token.Float(15.0, suffix))]
        expected_errors = []
        self.assert_cooks_to(raw_tokens, expected_tokens, expected_errors)

    def test_cooking_float_with_hex_prefix_produces_error(self):
        raw_tokens = [("0x1.0", raw_token.Number(16))]
        expected_tokens = [("0x1.0", cooked_token.Invalid())]
        expected_errors = [(0, hex_float_not_supported)]
        self.assert_cooks_to(raw_tokens, expected_tokens, expected_errors)

    def test_cooking_float_with_octal_prefix_produces_error(self):
        raw_tokens = [("0o1.0", raw_token.Number(8))]
        expected_tokens = [("0o1.0", cooked_token.Invalid())]
        expected_errors = [(0, octal_float_not_supported)]
        self.assert_cooks_to(raw_tokens, expected_tokens, expected_errors)

    def test_cooking_float_with_binary_prefix_produces_error(self):
        raw_tokens = [("0b1.0", raw_token.Number(2))]
        expected_tokens = [("0b1.0", cooked_token.Invalid())]
        expected_errors = [(0, binary_float_not_supported)]
        self.assert_cooks_to(raw_tokens, expected_tokens, expected_errors)

    def test_cooking_octal_literal_with_float_suffix_produces_error(self):
        raw_tokens = [("0o10f", raw_token.Number(8))]
        expected_tokens = [("0o10f", cooked_token.Invalid())]
        expected_errors = [(0, octal_float_not_supported)]
        self.assert_cooks_to(raw_tokens, expected_tokens, expected_errors)

    def test_coooking_binary_literal_with_float_suffix_produces_error(self):
        raw_tokens = [("0b10f", raw_token.Number(2))]
        expected_tokens = [("0b10f", cooked_token.Invalid())]
        expected_errors = [(0, binary_float_not_supported)]
        self.assert_cooks_to(raw_tokens, expected_tokens, expected_errors)

    def test_cooking_decimal_literal_with_invalid_digits_produces_error(self):
        raw_tokens = [("10a0", raw_token.Number(10))]
        expected_tokens = [("10a0", cooked_token.Invalid())]
        expected_errors = [(0, lambda t: invalid_number_suffix(t, "a0"))]
        self.assert_cooks_to(raw_tokens, expected_tokens, expected_errors)

    def test_cooking_hex_literal_with_invalid_digits_produces_error(self):
        raw_tokens = [("0xxd", raw_token.Number(16))]
        expected_tokens = [("0xxd", cooked_token.Invalid())]
        expected_errors = [(0, lambda t: invalid_number_suffix(t, "xd"))]
        self.assert_cooks_to(raw_tokens, expected_tokens, expected_errors)

    def test_cooking_octal_literal_with_invalid_digits_produces_error(self):
        raw_tokens = [("0o8", raw_token.Number(8))]
        expected_tokens = [("0o8", cooked_token.Invalid())]
        expected_errors = [(0, lambda t: invalid_number_suffix(t, "8"))]
        self.assert_cooks_to(raw_tokens, expected_tokens, expected_errors)

    def test_cooking_binary_literal_with_invalid_digits_produces_error(self):
        raw_tokens = [("0b3", raw_token.Number(2))]
        expected_tokens = [("0b3", cooked_token.Invalid())]
        expected_errors = [(0, lambda t: invalid_number_suffix(t, "3"))]
        self.assert_cooks_to(raw_tokens, expected_tokens, expected_errors)
