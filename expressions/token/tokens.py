from abc import ABC
from enum import Enum, auto
from string import ascii_letters

from expressions.token_groups import operators, constants, functions

OPERATORS = {'+': (1, lambda x, y: x + y), '-': (1, lambda x, y: x - y),
             '*': (2, lambda x, y: x * y), '/': (2, lambda x, y: x / y)}


def shunting_yard(parsed_formula):
    stack = []
    for token in parsed_formula:
        if token in OPERATORS:
            while stack and stack[-1] != "(" and OPERATORS[token][0] <= OPERATORS[stack[-1]][0]:
                yield stack.pop()
            stack.append(token)
        elif token == ")":
            while stack:
                x = stack.pop()
                if x == "(":
                    break
                yield x
        elif token == "(":
            stack.append(token)
        else:
            yield token
    while stack:
        yield stack.pop()


def calc(polish):
    stack = []
    for token in polish:
        if token in OPERATORS:
            y, x = stack.pop(), stack.pop()
            stack.append(OPERATORS[token][1](x, y))
        else:
            stack.append(token)
    return stack[0]


class TokenType(Enum):
    OPERATOR = auto()
    OPERAND = auto()
    VARIABLE = auto()
    BRACKET = auto()
    FUNCTION = auto()
    CONSTANT = auto()
    NONE = auto()


class Token(ABC):
    __value_type__ = type(None)
    __token_type__ = TokenType.NONE

    def __init__(self, value):
        self._validate(value)
        self.value = value

    def __repr__(self):
        return f'<{self.__class__.__name__} "{self.value}">'

    def __str__(self):
        return str(self.value)

    @property
    def type(self):
        return self.__token_type__

    def _validate(self, value):
        self._check_type(value)
        self._check_value(value)

    def _check_type(self, value):
        if not isinstance(value, self.__value_type__):
            raise TypeError(f'value must be of type {self.__value_type__.__name__}')

    def _check_value(self, value):
        pass


class Operator(Token):
    __value_type__ = str
    __token_type__ = TokenType.OPERATOR

    def _check_value(self, value: str):
        if len(value) != 1:
            raise ValueError(f'len(value) must be 1. value: "{value}" (len={len(value)})')
        if value not in operators:
            raise ValueError(f'value "{value}" is not an operator')


class Operand(Token):
    __value_type__ = float
    __token_type__ = TokenType.OPERAND


class Variable(Token):
    __value_type__ = str
    __token_type__ = TokenType.VARIABLE

    def _check_value(self, value: str):
        if len(value) != 1 or value not in ascii_letters:
            raise ValueError(f'variable must be an ascii letter of len = 1')


class Bracket(Token):
    __value_type__ = str
    __token_type__ = TokenType.BRACKET

    def _check_value(self, value: str):
        if len(value) != 1 or value not in '()':
            raise ValueError(f'bracket must be either "(" or ")"')


class Function(Token):
    __value_type__ = str
    __token_type__ = TokenType.FUNCTION

    def _check_value(self, value: str):
        if value not in functions:
            raise ValueError(f'bracket must be either "(" or ")"')


class Constant(Token):
    __value_type__ = str
    __token_type__ = TokenType.CONSTANT

    def _check_value(self, value: str):
        if value not in constants:
            raise ValueError(f'"{value}" is not a constant. Constants are: {tuple(constants)}')

