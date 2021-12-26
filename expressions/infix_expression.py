from typing import List, Dict

from .base_expression import BaseExpression, ExpressionType
from .errors import InvalidExpressionError
from .slib import Stack
from expressions.token import TokenType, Operand
from expressions.token import operators, constants


class InfixExpression(BaseExpression):
    __type__ = ExpressionType.INFIX

    def _eval(self):
        operators_stack = Stack()
        operands_stack = Stack()
        for token in self._tokens:
            if token.type == TokenType.OPERATOR:
                if not operators_stack:
                    operators_stack.push(token)
                elif token.priority > operators_stack.top().priority:
                    operators_stack.push(token)
                elif operands_stack.empty() or operands_stack.top().type == TokenType.BRACKET:
                    operators_stack.push(token)
                else:
                    while token.priority <= operators_stack.top().priority:
                        self._eval_on_stacks(operators_stack, operands_stack)
                        if not operators_stack:
                            operators_stack.push(token)
                            break
                    else:
                        operators_stack.push(token)
            elif token.type == TokenType.OPERAND:
                operands_stack.push(token)
            elif token.type == TokenType.VARIABLE:
                value = self._get_variable_value(token)
                operands_stack.push(Operand(float(value)))
            elif token.type == TokenType.CONSTANT:
                operands_stack.push(Operand(float(token())))
            elif token.type == TokenType.BRACKET:
                if token.value == '(':
                    operators_stack.push(token)
                    operands_stack.push(token)
                elif token.value == ')':
                    while operators_stack.top().value != '(':
                        self._eval_on_stacks(operators_stack, operands_stack)
                    operators_stack.pop()
                    # delete the bracket from operands stack     [4, ), 8, ...]
                    # this is value of expression inside brackets ^  ^
                    #                 this bracket should be removed |
                    v = operands_stack.pop()
                    operands_stack.pop()
                    operands_stack.push(v)
                    # apply function (if exists)
                    if not operators_stack:
                        continue
                    if operators_stack.top().type == TokenType.FUNCTION:
                        function_arg = operands_stack.pop().value
                        f = operators_stack.pop()
                        new_operand = Operand(f(function_arg))
                        operands_stack.push(new_operand)
            elif token.type == TokenType.FUNCTION:
                operators_stack.push(token)
        while operators_stack:
            self._eval_on_stacks(operators_stack, operands_stack)

        if len(operands_stack) > 1 or len(operators_stack) > 0:
            raise InvalidExpressionError()
        return operands_stack.top().value

    @staticmethod
    def _eval_on_stacks(operators_stack, operands_stack):
        '''
        Take 2 operands from operands stack
        and operator from operators stack
        and evaluate operation.

        If there are not enough operands, tries to take at least one.

        Leaves brackets in-place.

        :param operators_stack:
        :param operands_stack:
        :return:
        '''
        args = []

        if var2 := operands_stack.pop(default=None):
            if var2.type != TokenType.BRACKET:
                args.insert(0, var2.value)
            else:
                operands_stack.push(var2)

        if var1 := operands_stack.pop(default=None):
            if var1.type != TokenType.BRACKET:
                args.insert(0, var1.value)
            else:
                operands_stack.push(var1)

        operator_token = operators_stack.pop()
        op = operators.get(operator_token.value)

        if len(args) == 1:
            operator_token.unary = True

        new_operand = Operand(float(op(*args)))
        operands_stack.push(new_operand)

    def _pre_validate(self):
        previous_token = None
        for i, token in enumerate(self._tokens):
            if i == 0:
                if token.type == TokenType.OPERATOR and not token.possible_unary:
                    raise InvalidExpressionError(f'Expression starts with an non-unary operator {token.value}')
                previous_token = token
                continue
            if i == len(self._tokens) - 1:
                if token.type == TokenType.OPERATOR:
                    raise InvalidExpressionError(f'Expression ends with an operator {token.value}')
            if token.type == previous_token.type == TokenType.OPERATOR and not (token.possible_unary and previous_token.possible_unary):
                raise InvalidExpressionError(f'{token.value} following operator {previous_token.value}')
            if (
                token.type == previous_token.type == TokenType.OPERAND
                or token.type == previous_token.type == TokenType.VARIABLE
                or token.type == previous_token.type == TokenType.CONSTANT
            ):
                raise InvalidExpressionError(f'Two operands in a row in infix expression: {token}, {previous_token}')
            previous_token = token

