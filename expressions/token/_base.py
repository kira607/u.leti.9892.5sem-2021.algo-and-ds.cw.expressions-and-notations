from abc import ABC, abstractmethod
from enum import Enum, auto
from typing import Callable, Dict, Any, Optional

from expressions.slib import Stack


class TokenType(Enum):
    OPERATOR = auto()
    OPERAND = auto()
    VARIABLE = auto()
    BRACKET = auto()
    FUNCTION = auto()
    CONSTANT = auto()
    NONE = auto()


class Definition:
    pass


class Token(ABC):
    __value_type__ = type(None)
    __token_type__ = TokenType.NONE
    __group__ = None

    def __init__(self, value: __value_type__, callback: Callable = lambda: None, priority: int = None):
        self._validate(value)
        self._callback = callback
        self._priority = priority
        self.value = value

    def __repr__(self):
        return f'<{self.__class__.__name__} "{self.value}">'

    def __str__(self):
        return str(self.value)

    def __call__(self, *args, **kwargs):
        return self._callback(*args, **kwargs)

    @property
    def type(self):
        return self.__token_type__

    @property
    def priority(self) -> int:
        return self._priority

    def _validate(self, value):
        self._check_type(value)
        self._check_group(value)
        self._check_value(value)

    def _check_type(self, value):
        if not isinstance(value, self.__value_type__):
            raise TypeError(f'{self.__class__.__name__} value must be of type {self.__value_type__.__name__}')

    def _check_group(self, value):
        group = self.__group__
        if group:
            if value not in group:
                raise ValueError(
                    f'{self.__class__.__name__} accepts only values within {", ". join(str(gv) for gv in group)}'
                )

    def _check_value(self, value):
        pass


class TokenGroup(ABC):
    def __init__(self):
        self._iterator_indexes = Stack()
        self._group = self._define_group()
        self._iterable_group = tuple(self._group.keys())

    @abstractmethod
    def _define_group(self) -> Dict[str, Any]:
        pass

    @abstractmethod
    def get_token(self, value) -> Token:
        pass

    def __getitem__(self, key):
        return self._group[key]

    def __iter__(self):
        self._iterator_indexes.push(-1)
        return self

    def __next__(self):
        self._iterator_indexes.push(self._iterator_indexes.pop() + 1)
        if self._iterator_indexes.top() < len(self._iterable_group):
            return self._iterable_group[self._iterator_indexes.top()]
        else:
            self._iterator_indexes.pop()
            raise StopIteration()

    def get(self, string: str) -> Optional[Any]:
        return self._group.get(string)
