"""
Collection of tokens in lambda
"""


class Token:
    '''
    Generic token
    '''

    def __init__(self, text, location=None):
        self.text = text
        self.location = location

    def __eq__(self, other):
        return type(self) == type(other) and self.text == other.text

    def into(self, token_type):
        return token_type(self.text, self.location)


class Identifier(Token):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __repr__(self):
        return f"Identifier({self.text})"


class Number(Token):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __repr__(self):
        return f"Number({self.text})"


class String(Token):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __repr__(self):
        return f"String(\"{self.text}\")"


class Symbol(Token):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __repr__(self):
        return f"Symbol({self.text})"


class Comment(Token):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __repr__(self):
        return f"Comment({self.text})"


class Whitespace(Token):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __repr__(self):
        return f"Whitespace({self.text})"
