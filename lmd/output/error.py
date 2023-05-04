from lmd.util.error import *


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
        spans = sum([message.span.split() for message in messages], [])
        lines = [span.source.index_to_line_and_column(
            span.begin)[0] + 1 for span in spans]
        max_line_length = len(str(max(lines)))
        for message in messages:
            spans = message.span.split()
            for i, span in enumerate(spans):
                line_number, column = span.source.index_to_line_and_column(
                    span.begin)
                line = span.source.lines[line_number]
                prefix = f"{line_number + 1:>{max_line_length}} | "
                if i + 1 < len(spans):
                    underline_prefix = " " * max_line_length + " | " + " " * column
                else:
                    underline_prefix = " " * (len(prefix) + column)
                underline = underline_prefix + "^" * span.len()
                print(prefix + line)
                print(underline)

    def print_error_report(self, error_report):
        for error in error_report.errors:
            self.print_error(error)
