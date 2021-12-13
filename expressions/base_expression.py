from abc import ABC, abstractmethod
from typing import List, Generator

from expressions.token_groups.operator import operators
from expressions.token import TokenType, Tokenizer, Token


class BaseExpression(ABC):
    def __init__(self, expression: str):
        self._tokens = self.tokenize(expression)
        self.validated = tuple(self._parse())
        self._vars = {}

    def variables_names(self) -> Generator:
        for token in self._tokens:
            if token.type == TokenType.VARIABLE:
                yield token.value

    def set_variables(self, **variables):
        self._vars = variables

    @property
    def value(self):
        return self._eval()

    @abstractmethod
    def _parse(self) -> List:
        pass

    @abstractmethod
    def _eval(self) -> int:
        pass

    @staticmethod
    def get_type(symbol: str):
        if len(symbol) != 1:
            raise ValueError('symbol must be a string of a length of 1')
        if symbol in operators:
            return TokenType.OPERATOR

    @staticmethod
    def tokenize(expression: str) -> List[Token]:
        tokenizer = Tokenizer()
        return tokenizer.tokenize(expression)
