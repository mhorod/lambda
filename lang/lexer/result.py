class LexingError:
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


class LexingResult:
    def __init__(self, cursor, tokens, errors, fatal) -> None:
        self.cursor = cursor
        self.tokens = tokens
        self.errors = errors
        self.fatal = fatal

    def is_err(self):
        return self.fatal

    def is_ok(self):
        return not self.fatal

    def map(self, f):
        if not self.fatal:
            self.tokens = f(self.tokens)
        return self

    def map_err(self, f):
        if not self.fatal:
            self.errors = f(self.errors)
        return self

    def and_then_lex(self, lex):
        if not self.fatal:
            result = lex(self.cursor)
            return LexingResult(result.cursor, self.tokens + result.tokens, self.errors + result.errors, result.fatal)
        return self

    def and_then_transform(self, f):
        if not self.fatal:
            result = f(self.cursor, self.tokens)
            return LexingResult(result.cursor, result.tokens, self.errors + result.errors, result.fatal)
        return self


def Ok(cursor, tokens):
    ''''
    Return a lexing result with no errors
    '''
    if type(tokens) != list:
        tokens = [tokens]
    return LexingResult(cursor, tokens, [], False)


def Err(cursor, errors, fatal):
    '''
    Return a lexing result with errors
    '''
    if type(errors) != list:
        errors = [errors]
    return LexingResult(cursor, [], errors, fatal)
