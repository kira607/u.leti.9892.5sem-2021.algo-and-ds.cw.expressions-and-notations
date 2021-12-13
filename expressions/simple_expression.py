from typing import List, Dict

from .base_expression import BaseExpression
from .slib import Stack
from expressions.token.tokens import TokenType, Operand
from .token_groups import operators, constants


class SimpleExpression(BaseExpression):
    def _parse(self, ) -> List:
        parsed = []
        stack = Stack()
        for token in self._tokens:
            if token.type == TokenType.OPERATOR:
                tk = operators.get(token.value)
                while stack and stack.top() != '(' and tk.priority <= operators.get(stack.top().value).priority:
                    parsed.append(stack.pop())
                stack.push(token)
            elif token.value == ')':
                while stack:
                    x = stack.pop()
                    if x.value == '(':
                        break
                    parsed.append(x)
            elif token == '(':
                stack.push(token)
            else:
                parsed.append(token)
        while stack:
            parsed.append(stack.pop())
        return parsed

    def _eval(self):
        operators_stack = Stack()
        operands_stack = Stack()
        for token in self._tokens:
            if token.type == TokenType.OPERATOR:
                if not operators_stack:
                    operators_stack.push(token)
                elif operators.get(token.value).priority > operators.get(operators_stack.top().value).priority:
                    operators_stack.push(token)
                else:
                    while operators.get(token.value).priority <= operators.get(operators_stack.top().value).priority:
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
                operands_stack.push(Operand(float(constants.get(token.value).value)))
            elif token.type == TokenType.BRACKET:
                if token.value == '(':
                    operators_stack.push(token)
                elif token.value == ')':
                    while operators_stack.top().value != '(':
                        self._eval_on_stacks(operators_stack, operands_stack)
                    operators_stack.pop()
        while operators_stack:
            self._eval_on_stacks(operators_stack, operands_stack)
        return operands_stack.top().value

    def _eval_on_stacks(self, operators_stack, operands_stack):
        var2 = operands_stack.pop().value
        var1 = operands_stack.pop().value
        op = operators.get(operators_stack.pop().value)
        operands_stack.push(Operand(float(op(var1, var2))))

    def _get_variable_value(self, token):
        var_name = token.value
        value = self._vars.get(var_name)
        if value is None:
            raise RuntimeError(f'Variable "{var_name}" is not defined')
        return value
