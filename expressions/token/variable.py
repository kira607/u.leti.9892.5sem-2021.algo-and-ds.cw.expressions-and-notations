from string import ascii_letters

from ._base import Token
from ._base import TokenType


class Variable(Token):
    __value_type__ = str
    __token_type__ = TokenType.VARIABLE

    def _check_value(self, value: __value_type__):
        if len(value) != 1 or value not in ascii_letters:
            raise ValueError(f'variable must be an ascii letter of len = 1')