from typing import Callable, Dict

from ._base import Token
from ._base import Definition
from ._base import TokenType
from ._base import TokenGroup


class OperatorDefinition(Definition):
    def __init__(self, operator: str, priority: int, callback: Callable = lambda: None, possible_unary: bool = False):
        self._string = operator
        self._priority = priority
        self._callback = callback
        self.possible_unary = possible_unary

    def __call__(self, *args, **kwargs):
        return self._callback(*args, **kwargs)

    def __str__(self) -> str:
        return self._string

    @property
    def priority(self) -> int:
        return self._priority

    @property
    def callback(self) -> Callable:
        return self._callback


class Operators(TokenGroup):
    def _define_group(self) -> Dict[str, OperatorDefinition]:
        return {
            '+': OperatorDefinition('+', 1, lambda x, y=None: x if y is None else x + y, True),
            '-': OperatorDefinition('-', 1, lambda x, y=None: -x if y is None else x - y, True),
            '*': OperatorDefinition('*', 2, lambda x, y: x * y),
            '/': OperatorDefinition('/', 2, lambda x, y: x / y),
            '%': OperatorDefinition('%', 2, lambda x, y: x % y),
            '//': OperatorDefinition('//', 2, lambda x, y: x // y),
            '^': OperatorDefinition('^', 3, lambda x, y: x ** y),
        }

    def get_token(self, operator_string: str) -> 'Operator':
        operator_data = self._group.get(operator_string)
        callback = operator_data.callback
        priority = operator_data.priority
        possible_unary = operator_data.possible_unary
        return Operator(operator_string, callback=callback, priority=priority, possible_unary=possible_unary)


operators = Operators()


class Operator(Token):
    __value_type__ = str
    __token_type__ = TokenType.OPERATOR
    __group__ = operators

    def __init__(
        self,
        value: __value_type__,
        callback: Callable = lambda: None,
        priority: int = None,
        possible_unary: bool = False,
        unary: bool = False,
    ):
        self.possible_unary = possible_unary
        self.unary = unary
        super(Operator, self).__init__(value, callback, priority)

    def _check_value(self, value: __value_type__):
        if len(value) > 2:
            raise ValueError(f'len(value) must <= 2. value: "{value}" (len={len(value)})')
