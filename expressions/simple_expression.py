from .base_expression import BaseExpression

class SimpleExpression(BaseExpression):
    def _parse(self, expression: str) -> None:
        for symbol in expression:
            pass
