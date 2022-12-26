from dataclasses import dataclass
from enum import Enum, auto

import lmd.source

class KeywordKind(Enum):
    Let = auto()


@dataclass
class Token:
    span: lmd.source.Span