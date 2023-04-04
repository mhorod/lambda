from typing import List

from lmd import source


class Message:
    def __init__(self, span, comment):
        self.span = span
        self.comment = comment


class Error:
    def __init__(self, reason: Message, messages: List[Message] = None):
        self.reason = reason
        self.messages = messages or []


class ErrorReport:
    def __init__(self):
        self.errors = []

    def add(self, error):
        self.errors.append(error)

    def has_errors(self):
        return len(self.errors) > 0


class SimpleErrorPrinter:
    def print(self, error_report):
        for error in error_report.errors:
            self.print_error(error)

    def print_error(self, error):
        span = error.reason.span
        line, column = span.source.index_to_line_and_column(span.begin)
        print(f"error: {error.reason.comment}")
        print(
            f"--> file {span.source.name} at line {line + 1}, column {column + 1}")

        if error.messages:
            self.print_messages(error.messages)
        else:
            self.print_messages([Message(span, "")])

    def print_messages(self, messages):
        lines = [message.span.source.index_to_line_and_column(
            message.span.begin)[0] for message in messages]
        max_line_length = len(str(max(lines)))
        for message in messages:
            line_number, column = message.span.source.index_to_line_and_column(
                message.span.begin)
            line = message.span.source.lines[line_number]
            prefix = f"{line_number + 1:>{max_line_length}} | "

            underline = " " * (len(prefix) + column) + "^" * message.span.len()
            print(prefix + line)
            print(underline)

    def print_error_report(self, error_report):
        for error in error_report.errors:
            self.print_error(error)
