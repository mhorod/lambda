from dataclasses import dataclass

import bisect


class Source:
    def __init__(self, name, text):
        self.name = name
        self.text = text

        self.lines = self.text.splitlines()
        self.line_lengths = [len(line) for line in self.lines]
        self.prefix_sums = [0]
        for line_length in self.line_lengths:
            self.prefix_sums.append(line_length + self.prefix_sums[-1] + 1)

    def index_to_line_and_column(self, index):
        line = bisect.bisect_right(self.prefix_sums, index) - 1
        column = index - self.prefix_sums[line]
        return line, column

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

    def len(self):
        return self.end - self.begin


@dataclass
class LineCol:
    source: Source
    line: int
    column: int
