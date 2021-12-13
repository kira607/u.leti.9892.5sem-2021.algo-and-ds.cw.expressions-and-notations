from typing import Callable, Dict

from expressions.token_groups.token_group import TokenGroup


class OperatorT:
    def __init__(self, operator: str, priority: int, callback: Callable = lambda: None):
        self._string = operator
        self._priority = priority
        self._callback = callback

    def __call__(self, *args, **kwargs):
        return self._callback(*args, **kwargs)

    def __str__(self) -> str:
        return self._string

    @property
    def priority(self) -> int:
        return self._priority


class Operators(TokenGroup):
    def _define_group(self) -> Dict[str, OperatorT]:
        return {
            '+': OperatorT('+', 1, lambda x, y: x + y),
            '-': OperatorT('-', 1, lambda x, y: x - y),
            '*': OperatorT('*', 2, lambda x, y: x * y),
            '/': OperatorT('/', 2, lambda x, y: x / y),
            '^': OperatorT('^', 3, lambda x, y: x ** y),
            ')': OperatorT(')', 0),
            '(': OperatorT('(', 0),
        }


operators = Operators()
