from abc import ABC, abstractmethod
from typing import Callable, List
from enum import Enum, auto

from dataclasses import dataclass

from lmd.util.token import *
from lmd.util.error import *

from lmd.parsing.cursor import Cursor


class ParsingState(Enum):
    '''
    The state of parsing.
    OK - The parsing parsed successfully.
    BACKTRACKED - The parsing backtracked and it's ready to continue
    ERR - The parsing failed and should be handled by the caller.
    '''
    OK = auto()
    BACKTRACKED = auto()
    ERR = auto()


class Result:
    def __init__(self, cursor, values, errors, state):
        self.cursor = cursor
        self.values = values
        self.errors = errors
        self.state = state

    def Ok(cursor, values, errors):
        return Result(cursor, values, errors, ParsingState.OK)

    def Backtracked(cursor, values, errors):
        return Result(cursor, values, errors, ParsingState.BACKTRACKED)

    def Err(cursor, values, errors):
        return Result(cursor, values, errors, ParsingState.ERR)

    def map(self, f):
        if self.state == ParsingState.OK:
            return Result.Ok(self.cursor, [f(self.values)], self.errors)
        else:
            return self

    def __repr__(self):
        return f'Result({self.state}, {self.cursor}, {self.values}, {self.errors})'


class Parser(ABC):
    @abstractmethod
    def parse(self, cursor: Cursor, backtrack=False) -> Result:
        pass

    def __or__(self, other):
        return Or([self, other])

    def __add__(self, other):
        return Sequential([self, other])

    def __rshift__(self, other):
        return Conditional(self, other)


class Conditional(Parser):
    '''
    Conditional parser. condition >> then

    If condition parses successfully, then is executed.
    Otherwise, the parser backtracks.

    The result of the parser is a list of the results of condition and then.
    '''

    def __init__(self, condition: Parser, then: Parser):
        self.condition = condition
        self.then = then

    def parse(self, cursor: Cursor, backtrack=False) -> Result:
        condition_result = self.condition.parse(cursor.clone(), backtrack)
        if condition_result.state == ParsingState.OK:
            then_result = self.then.parse(condition_result.cursor, backtrack)
            then_result.values = condition_result.values + then_result.values
            then_result.errors = condition_result.errors + then_result.errors
            return then_result
        else:
            return condition_result


class Or(Parser):
    def __init__(self, parsers: List[Parser]):
        self.parsers = parsers

    def parse(self, cursor: Cursor, backtrack=False) -> Result:
        for i, parser in enumerate(self.parsers):
            if i == len(self.parsers) - 1:
                return parser.parse(cursor, backtrack)
            else:
                result = parser.parse(cursor.clone(), True)
                if result.state != ParsingState.BACKTRACKED:
                    return result

    def __or__(self, other):
        return Or(self.parsers + [other])


class Sequential(Parser):
    def __init__(self, parsers: List[Parser]):
        self.parsers = parsers

    def __add__(self, other):
        return Sequential(self.parsers + [other])

    def parse(self, cursor: Cursor, backtrack=False) -> Result:
        values = []
        errors = []
        err = False
        for parser in self.parsers:
            if err:
                values.append(None)
            else:
                result = parser.parse(cursor.clone(), backtrack=False)
                values += result.values
                errors += result.errors
                cursor = result.cursor

                if result.state != ParsingState.OK:
                    err = True

        if err:
            return Result.Err(cursor, values, errors)
        else:
            return Result.Ok(cursor, values, errors)


class Drop(Parser):
    def __init__(self, parser: Parser):
        self.parser = parser

    def parse(self, cursor: Cursor, backtrack=False) -> Result:
        result = self.parser.parse(cursor, backtrack)
        result.values = []
        return result


class Maybe(Parser):
    def __init__(self, parser: Parser):
        self.parser = parser

    def parse(self, cursor: Cursor, backtrack=False) -> Result:
        result = self.parser.parse(cursor.clone(), backtrack)
        if result.state == ParsingState.OK:
            return result
        else:
            return Result.Ok(cursor, [], [])


class Repeat(Parser):
    def __init__(self, parser: Parser):
        self.parser = parser

    def parse(self, cursor: Cursor, backtrack=False) -> Result:
        values = []
        errors = []
        while True:
            result = self.parser.parse(cursor.clone(), backtrack=False)
            if result.state != ParsingState.OK:
                return Result.Ok(cursor, values, errors)
            else:
                values += result.values
                errors += result.errors
                cursor = result.cursor


class Do(Parser):
    def __init__(self, function: Callable[[Cursor], Result]):
        self.function = function

    def parse(self, cursor: Cursor, backtrack=False) -> Result:
        result = self.function(cursor)
        if result.state != ParsingState.ERR:
            return result
        elif backtrack:
            return Result.Backtracked(cursor, [], [])
        else:
            return result
