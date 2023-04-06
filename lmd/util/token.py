'''
Generic token i.e. segment of source code with some description
'''

from dataclasses import dataclass

from lmd.util.source import Span


class TokenKind:
    def __init__(self, token_type):
        self.token_type = token_type

    def extends(self, base):
        if not isinstance(self, type(base)):
            return False
        for attr, base_value in base.kind_attrs().items():
            if getattr(self, attr) != base_value:
                return False
        return True

    def kind_attrs(self):
        '''
        Get attributes that describe the kind 
        '''
        return {
            k: self.__dict__[k]
            for k in self.__dict__.keys()
            if not k.startswith('_')
        }

    def __str__(self):
        return f"{type(self).__name__}"

    def __repr__(self):
        return f"{type(self).__name__}({self.kind_attrs()})"

    def __eq__(self, other):
        return self.kind_attrs() == other.kind_attrs()


@dataclass
class Token:
    span: Span
    kind: TokenKind
    text: str

    def __str__(self):
        return f'{self.span}: {self.kind} {repr(self.text)}'
