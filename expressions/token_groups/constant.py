import math
from typing import Dict

from expressions.token_groups.token_group import TokenGroup


class ConstantT:
    def __init__(self, name: str, value: float):
        self._name = name
        self._value = value

    def __str__(self) -> str:
        return str(self._name)

    @property
    def value(self):
        return self._value


class Constants(TokenGroup):
    def _define_group(self) -> Dict[str, ConstantT]:
        return {
            'pi': ConstantT('pi', math.pi),
            'e': ConstantT('e', math.e),
        }


constants = Constants()
