import math
from typing import Callable, Dict

from ._base import Token
from ._base import Definition
from ._base import TokenType
from ._base import TokenGroup


class FunctionDefinition(Definition):
    def __init__(self, name: str, callback: Callable = lambda: None):
        self._name = name
        self._callback = callback

    def __call__(self, *args, **kwargs):
        return self._callback(*args, **kwargs)

    def __str__(self) -> str:
        return self._name

    @property
    def callback(self) -> Callable:
        return self._callback


class Functions(TokenGroup):
    def _define_group(self) -> Dict[str, FunctionDefinition]:
        return {
            'cos': FunctionDefinition('cos', lambda x: math.cos(x)),
            'sin': FunctionDefinition('sin', lambda x: math.sin(x)),
            'tg': FunctionDefinition('tg', lambda x: math.tan(x)),
            'ctg': FunctionDefinition('ctg', lambda x: math.cos(x) / math.sin(x)),
            'ln': FunctionDefinition('ln', lambda x: math.log(x)),
            'lg': FunctionDefinition('log', lambda x: math.log10(x)),
            'sqrt': FunctionDefinition('sqrt', lambda x: math.sqrt(x)),

            'log2': FunctionDefinition('log2', lambda x: math.log2(x)),
            'abs': FunctionDefinition('abs', lambda x: math.fabs(x)),
            'fact': FunctionDefinition('fact', lambda x: float(math.factorial(int(x))))
        }

    def get_token(self, function_string) -> 'Function':
        callback = self._group[function_string].callback
        return Function(function_string, callback, priority=-1)


functions = Functions()


class Function(Token):
    __value_type__ = str
    __token_type__ = TokenType.FUNCTION
    __group__ = functions
