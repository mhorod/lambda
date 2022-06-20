"""
Collection of tokens in lambda
"""


class Token:
    def __init__(self, text):
        self.text = text

    def __eq__(self, other):
        return type(self) == type(other) and self.text == other.text


class Identifier(Token):
    def __init__(self, text):
        self.text = text

    def __repr__(self):
        return f"Identifier({self.text})"


class Number(Token):
    def __init__(self, text):
        self.text = text

    def __repr__(self):
        return f"Number({self.text})"


class String(Token):
    def __init__(self, text):
        self.text = text

    def __repr__(self):
        return f"String(\"{self.text}\")"


class Symbol(Token):
    def __init__(self, text):
        self.text = text

    def __repr__(self):
        return f"Symbol({self.text})"


class Comment(Token):
    def __init__(self, text):
        self.text = text

    def __repr__(self):
        return f"Comment(self.text)"
