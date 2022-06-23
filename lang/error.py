
class Error:
    def __init__(self, message, location):
        self.message = message
        self.location = location

    def __str__(self):
        return f"{self.location}:\n {self.message}"

    def print(self):
        print_error(self)


def print_error(error):
    line = error.location.source.linecol(error.location.begin).line + 1
    column = error.location.source.linecol(error.location.begin).column + 1
    print(f"{error.location}:")
    print(error.location.source.lines[line - 1])
    print(" " * (column - 1) + error.location.len() * "^")
    print(error.message)
