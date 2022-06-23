from dataclasses import dataclass


class Source:
    def __init__(self, name, text):
        self.name = name
        self.text = text
        self.lines = text.split('\n')
        self.line_starts = [0]
        for line in self.lines:
            self.line_starts.append(self.line_starts[-1] + len(line) + 1)

    def len(self):
        return len(self.text)

    def __getitem__(self, index):
        return self.text[index]

    def linecol(self, index):
        line = 0
        for i in range(index):
            if self.text[i] == '\n':
                line += 1
        return LineCol(line, index - self.line_starts[line])


@dataclass
class LineCol:
    line: int
    column: int


@dataclass
class Location:
    source: Source
    begin: int
    end: int

    def __str__(self):
        linecol = self.source.linecol(self.begin)
        return f"File {self.source.name}, line {linecol.line + 1}, column {linecol.column + 1}"

    def len(self):
        return self.end - self.begin
