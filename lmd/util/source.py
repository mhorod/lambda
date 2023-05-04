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

    def split_span(self, begin, end):
        begin_line, begin_column = self.index_to_line_and_column(begin)
        end_line, end_column = self.index_to_line_and_column(end)

        if begin_line == end_line:
            return [Span(self, begin, end)]

        spans = []
        spans.append(Span(self, begin, self.prefix_sums[begin_line + 1] - 1))
        for line in range(begin_line + 1, end_line):
            spans.append(
                Span(self, self.prefix_sums[line], self.prefix_sums[line + 1] - 1))
        spans.append(Span(self, self.prefix_sums[end_line], end))
        return spans

    def len(self):
        return len(self.text)

    def __getitem__(self, index):
        return self.text[index]

    def from_file(path: str) -> 'Source':
        with open(path, 'r') as f:
            return Source(path, f.read())


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

    def split(self):
        return self.source.split_span(self.begin, self.end)


def wrapping_span(spans):
    begin = min(span.begin for span in spans)
    end = max(span.end for span in spans)
    return Span(spans[0].source, begin, end)


@dataclass
class LineCol:
    source: Source
    line: int
    column: int
