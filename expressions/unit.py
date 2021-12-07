from enum import Enum, auto


class UnitType(Enum):
    OPERATOR = auto()
    OPERAND = auto()
    VARIABLE = auto()
    BRACKET = auto()
    NONE = auto()


class Unit:
    def __init__(self, value, type_):
        self.value = value
        self.type = type_


class OperatorUnit:
    def __init__(self, operator: str, priority: int):
        self._string = operator
        self._priority = priority

    def __str__(self) -> str:
        return self._string

    @property
    def priority(self) -> int:
        return self._priority


class Operators:
    def __init__(self):
        self._iterator_index = -1
        self._operators = {
            '+': OperatorUnit('+', 1),
            '-': OperatorUnit('-', 1),
            '*': OperatorUnit('*', 2),
            '/': OperatorUnit('/', 2),
            '^': OperatorUnit('^', 3),
            ')': OperatorUnit(')', 0),
            '(': OperatorUnit('(', 0),
        }

    def __getitem__(self, key):
        return self._operators[key]

    def __iter__(self):
        return self

    def __next__(self):
        self._iterator_index += 1
        if self._iterator_index < len(self._operators):
            return self._operators[self._iterator_index]
        else:
            self._iterator_index = -1
            raise StopIteration()

operators = Operators()