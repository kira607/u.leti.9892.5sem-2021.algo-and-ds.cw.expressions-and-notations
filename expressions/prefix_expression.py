from expressions import BaseExpression
from expressions.errors import InvalidExpressionError
from expressions.slib import Stack
from expressions.token import TokenType, operators, Operand, functions


class PrefixExpression(BaseExpression):
    def _eval(self) -> int:
        operands_stack = Stack()
        for token in self._tokens[::-1]:
            if token.type == TokenType.OPERATOR:
                x = operands_stack.pop().value
                y = operands_stack.pop(default=None)
                y = y.value if y else None
                op = operators.get(token.value)
                value = op(x, y) if y else op(x)
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
            elif token.type == TokenType.DELIMITER:
                raise InvalidExpressionError(f'{self.__class__.__name__} cannot have delimiters')
            elif token.type == TokenType.FUNCTION:
                x = operands_stack.pop().value
                f = functions.get(token.value)
                value = f(x)
                new_operand = Operand(value)
                operands_stack.push(new_operand)

        if len(operands_stack) > 1:
            raise InvalidExpressionError()

        return operands_stack.top().value