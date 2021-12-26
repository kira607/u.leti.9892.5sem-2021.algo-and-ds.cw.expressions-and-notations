from .base_expression import BaseExpression
from .base_expression import ExpressionType
from .errors import InvalidExpressionError
from .slib import Stack
from .token import TokenType, operators, Operand, functions


class PostfixExpression(BaseExpression):
    __type__ = ExpressionType.POSTFIX

    def _eval(self) -> int:
        operands_stack = Stack()
        for token in self._tokens:
            if token.type == TokenType.OPERATOR:
                y = operands_stack.pop().value
                x = operands_stack.pop(default=None)
                x = x.value if x else None
                op = operators.get(token.value)
                if x:
                    value = op(x, y)
                else:
                    token.unary = True
                    value = op(y)
                new_operand = Operand(value)
                operands_stack.push(new_operand)
            elif token.type == TokenType.OPERAND:
                operands_stack.push(token)
            elif token.type == TokenType.VARIABLE:
                value = self._get_variable_value(token)
                operands_stack.push(Operand(float(value)))
            elif token.type == TokenType.CONSTANT:
                operands_stack.push(Operand(float(token())))
            elif token.type == TokenType.BRACKET:
                raise InvalidExpressionError(f'{self.__class__.__name__} cannot have brackets')
            elif token.type == TokenType.FUNCTION:
                x = operands_stack.pop().value
                f = functions.get(token.value)
                value = f(x)
                new_operand = Operand(value)
                operands_stack.push(new_operand)

        if len(operands_stack) > 1:
            raise InvalidExpressionError()

        return operands_stack.top().value
