
class Message:
    def __init__(self, span, comment):
        self.span = span
        self.comment = comment


class Error:
    def __init__(self, messages):
        self.messages = messages


class ErrorReport:
    def __init__(self):
        self.errors = []

    def add(self, error):
        self.errors.append(error)


class SimpleErrorPrinter:
    def print(self, error_report):
        for error in error_report.errors:
            for message in error.messages:
                print(message.comment + " at " + str(message.span))
