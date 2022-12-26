from dataclasses import dataclass


class Source:
    def __init__(self, name, text):
        self.name = name
        self.text = text
    
    def len(self):
        return len(self.text)

    def __getitem__(self, index):
        return self.text[index]

@dataclass
class LineColumn:
    line: int
    column: int


@dataclass
class Span:
    source: Source
    begin: int
    end: int

    def __repr__(self):
        return f"{self.source.name}:{self.begin}:{self.end}"