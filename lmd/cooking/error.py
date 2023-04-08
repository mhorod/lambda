from lmd.util.error import *


def unterminated_string(token):
    message = Message(token.span, f"Unterminated string")
    return Error(message)


def unterminated_comment(token):
    message = Message(token.span, f"Unterminated comment")
    return Error(message)


def unknown_token(token):
    message = Message(token.span, f"Unknown token: `{token.text}`")
    return Error(message)


def number_without_digits(token):
    message = Message(token.span, f"Number without digits")
    return Error(message)


def invalid_number_suffix(token, suffix):
    message = Message(token.span, f"Invalid number suffix: `{suffix}`")
    return Error(message)


def hex_float_not_supported(token):
    message = Message(
        token.span, f"Hexadecimal float literals are not supported")
    return Error(message)


def octal_float_not_supported(token):
    message = Message(
        token.span, f"Octal float literals are not supported")
    return Error(message)


def binary_float_not_supported(token):
    message = Message(token.span, f"Binary float literals are not supported")
    return Error(message)


def invalid_float_literal(token):
    message = Message(token.span, f"Invalid float literal: `{token.text}`")
    return Error(message)
