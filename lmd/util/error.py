from typing import List
from dataclasses import dataclass

from lmd.util.source import Span


@dataclass
class Message:
    span: Span
    comment: str


@dataclass
class Error:
    reason: Message
    messages: List[Message] = None


class ErrorReport:
    def __init__(self):
        self.errors = []

    def add(self, error):
        self.errors.append(error)

    def error(self, error):
        self.errors.append(error)

    def has_errors(self):
        return len(self.errors) > 0
