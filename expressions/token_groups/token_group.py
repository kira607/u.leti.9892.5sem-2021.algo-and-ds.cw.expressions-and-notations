from abc import ABC, abstractmethod
from typing import Dict, Any, Optional

from expressions.slib import Stack


class TokenGroup(ABC):
    def __init__(self):
        self._iterator_indexes = Stack()
        self._group = self._define_group()
        self._iterable_group = tuple(self._group.keys())

    @abstractmethod
    def _define_group(self) -> Dict[str, Any]:
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
