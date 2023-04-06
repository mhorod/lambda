from lmd.util.source import *


class Cursor:
    '''
    Cursor that points to a position in a source.
    '''

    def __init__(self, src: Source, index: int = 0):
        self.src = src
        self.index = index
        self.consumed_begin = index

    def peek(self, cnt: int = 1) -> str:
        '''
        Peek at the next `cnt` characters
        '''
        return self.src[self.index:self.index + cnt]

    def take(self, cnt: int = 1) -> str:
        '''
        Take the next `cnt` characters
        '''
        result = self.peek(cnt)
        self.index += cnt
        return result

    def take_while(self, predicate) -> str:
        '''
        Take characters while `predicate` returns true
        '''
        result = ""
        while self.has() and predicate(self.peek()):
            result += self.take()
        return result

    def has(self, cnt: int = 1) -> bool:
        '''
        Check if there are `cnt` characters left
        '''
        return self.index + cnt <= self.src.len()

    def consume_span(self) -> Span:
        '''
        Consume the span from the last `consume_span` call to now.
        '''
        result = Span(self.src, self.consumed_begin, self.index)
        self.consumed_begin = self.index
        return result
