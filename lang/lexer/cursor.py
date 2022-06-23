from lang.source import Source, Location


class Cursor:
    def __init__(self, source: Source, index=0) -> None:
        self.source = source
        self.index = index
        self.start_index = index

    def peek(self, count=1) -> str:
        '''
        Peek ahead `count` characters
        '''
        text = self.source[self.index:self.index+count]
        return text

    def peek_while(self, predicate: callable, limit=None) -> str:
        '''
        Peek ahead while `predicate` is true
        '''
        text = ""
        count = 0
        while self.remaining() > count and predicate(self.peek(count + 1)[-1]) and (limit is None or len(text) < limit):
            text = self.peek(count + 1)
            count += 1
        return text

    def advance(self, count=1) -> None:
        self.index += count

    def take(self, count=1) -> str:
        '''
        Take `count` characters
        '''
        text = self.source[self.index:self.index+count]
        self.advance(count)
        return text

    def consumed_location(self):
        return Location(self.source, self.start_index, self.index)

    def remaining(self):
        return self.source.len() - self.index

    def has(self, count=1) -> bool:
        return self.index + count <= self.source.len()

    def clone(self):
        '''
        Clone this cursor with reset consumed location
        '''
        return Cursor(self.source, self.index)

    def take_while(self, predicate: callable, limit=None) -> str:
        '''
        Take characters while `predicate` is true
        '''
        text = ""
        while self.has() and predicate(self.peek()) and (limit is None or len(text) < limit):
            text += self.take()
        return text
