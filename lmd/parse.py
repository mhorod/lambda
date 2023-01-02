from typing import List

from lmd import lex
from lmd.tokens import *
from lmd.errors import *


def cook_tokens(tokens: List[lex.RawToken], error_report: ErrorReport) -> List[Token]:
    cooked = []
    for token in tokens:
        pass
