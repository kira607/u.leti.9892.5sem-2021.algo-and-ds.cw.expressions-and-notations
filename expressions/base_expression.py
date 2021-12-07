from abc import ABC, abstractmethod
from .unit import OperatorUnit, UnitType, operators


class BaseExpression(ABC):
    def __init__(self, expression: str):
        self._data = None
        self._parse(expression)

    def reset(self) -> None:
        pass

    @abstractmethod
    def _parse(self, expression: str) -> None:
        pass

    @staticmethod
    def get_type(symbol: str):
        if len(symbol) != 1:
            raise ValueError('symbol must be a string of a length of 1')
        if symbol in operators:
            return UnitType.OPERATOR