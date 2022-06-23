class ParsingResult:
    '''
    Result of parsing or lexing tokens from a cursor
    '''

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

    def and_then(self, f):
        if not self.fatal:
            result = f(self.cursor)
            return ParsingResult(result.cursor, self.tokens + result.tokens, self.errors + result.errors, result.fatal)
        return self

    def and_then_transform(self, f):
        if not self.fatal:
            result = f(self.cursor, self.tokens)
            return ParsingResult(result.cursor, result.tokens, self.errors + result.errors, result.fatal)
        return self


def Ok(cursor, tokens):
    ''''
    Return a lexing result with no errors
    '''
    if type(tokens) != list:
        tokens = [tokens]
    return ParsingResult(cursor, tokens, [], False)


def Err(cursor, errors, fatal):
    '''
    Return a lexing result with errors
    '''
    if type(errors) != list:
        errors = [errors]
    return ParsingResult(cursor, [], errors, fatal)
