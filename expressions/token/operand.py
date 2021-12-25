from ._base import Token
from ._base import TokenType


class Operand(Token):
    __value_type__ = float
    __token_type__ = TokenType.OPERAND
