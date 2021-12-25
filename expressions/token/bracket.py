from typing import Dict

from ._base import Token
from ._base import Definition
from ._base import TokenType
from ._base import TokenGroup


class BracketDefinition(Definition):
    def __init__(self, bracket: str):
        self.bracket = bracket

    def __str__(self) -> str:
        return str(self.bracket)

    @property
    def value(self):
        return self.bracket


class Brackets(TokenGroup):
    def _define_group(self) -> Dict[str, BracketDefinition]:
        return {
            '(': BracketDefinition('('),
            ')': BracketDefinition(')'),
        }

    def get_token(self, bracket_string: str) -> 'Bracket':
        return Bracket(bracket_string, priority=0)


brackets = Brackets()


class Bracket(Token):
    __value_type__ = str
    __token_type__ = TokenType.BRACKET
    __group__ = brackets
