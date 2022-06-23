from .tokens import Whitespace, Comment


class TokenCursor:
    def __init__(self, data):
        self.data = [token for token in data if type(
            token) not in (Whitespace, Comment)]
        self.index = 0

    def has(self):
        return self.index < len(self.data)

    def peek(self, count=1):
        tokens = self.data[self.index:self.index + count]
        if len(tokens) == 1:
            return tokens[0]
        else:
            return tokens

    def consume(self, count=1):
        consumed = self.peek(count)
        self.skip(count)
        return consumed

    def skip(self, count=1):
        self.index += count
