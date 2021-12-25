import math
from typing import Dict

from ._base import Token
from ._base import Definition
from ._base import TokenType
from ._base import TokenGroup


class ConstantDefinition(Definition):
    def __init__(self, name: str, value: float):
        self._name = name
        self._value = value

    def __str__(self) -> str:
        return str(self._name)

    @property
    def value(self):
        return self._value


class Constants(TokenGroup):
    def _define_group(self) -> Dict[str, ConstantDefinition]:
        return {
            'pi': ConstantDefinition('pi', math.pi),
            'e': ConstantDefinition('e', math.e),
        }

    def get_token(self, constant_string) -> 'Constant':
        return Constant(constant_string, lambda: self._group[constant_string].value)


constants = Constants()


class Constant(Token):
    __value_type__ = str
    __token_type__ = TokenType.CONSTANT
    __group__ = constants
