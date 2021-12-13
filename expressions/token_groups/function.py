import math
from typing import Callable, Dict

from expressions.token_groups.token_group import TokenGroup


class FunctionT:
    def __init__(self, name: str, callback: Callable = lambda: None):
        self._name = name
        self._callback = callback

    def __call__(self, *args, **kwargs):
        return self._callback(*args, **kwargs)

    def __str__(self) -> str:
        return self._name


class Functions(TokenGroup):
    def _define_group(self) -> Dict[str, FunctionT]:
        return {
            'cos': FunctionT('cos', lambda x: math.cos(x)),
            'sin': FunctionT('sin', lambda x: math.sin(x)),
            'tg': FunctionT('tg', lambda x: math.tan(x)),
            'ctg': FunctionT('ctg', lambda x: math.cos(x) / math.sin(x)),
            'ln': FunctionT('ln', lambda x: math.log(x)),
            'log': FunctionT('log', lambda x, base: math.log(x, base)),
            'sqrt': FunctionT('sqrt', lambda x: math.sqrt(x)),

            'abs': FunctionT('abs', lambda x: math.fabs(x)),
            'lg': FunctionT('lg', lambda x: math.log10(x)),
        }


functions = Functions()
