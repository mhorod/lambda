from typing import List

from lmd.cooking.tokens import Eof
from lmd.util.token import Token


class Cursor:
    def __init__(self, tokens: List[Token], index: int = 0):
        self.tokens = tokens
        self.index = index
        self.consumed_begin = index

    def clone(self) -> "Cursor":
        return Cursor(self.tokens, self.index)

    def has(self, cnt: int = 1) -> bool:
        return self.index + cnt <= len(self.tokens)

    def peek_one(self) -> Token:
        if not self.has():
            return self.eof()
        else:
            return self.tokens[self.index]

    def eof(self) -> bool:
        return Token(self.tokens[-1].span, Eof(), "<eof>")

    def peek(self, cnt: int = 1) -> List[Token]:
        return self.tokens[self.index:self.index + cnt]

    def prev(self) -> Token:
        return self.tokens[self.index - 1]

    def take_one(self) -> Token:
        result = self.peek_one()
        self.index += 1
        return result

    def take(self, cnt: int = 1) -> List[Token]:
        result = self.peek(cnt)
        self.index += cnt
        return result
