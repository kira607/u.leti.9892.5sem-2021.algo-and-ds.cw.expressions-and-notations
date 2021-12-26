from expressions.slib import Stack
from expressions.token import TokenType, brackets
from .base_expression import ExpressionType, BaseExpression
from .errors import InvalidExpressionError
from .postfix_expression import PostfixExpression
from .prefix_expression import PrefixExpression
from .infix_expression import InfixExpression


class Converter:
    def __init__(self):
        self._converters = {
            (ExpressionType.INFIX, ExpressionType.INFIX): lambda x: x,
            (ExpressionType.INFIX, ExpressionType.PREFIX): self.infix_to_prefix,
            (ExpressionType.INFIX, ExpressionType.POSTFIX): self.infix_to_postfix,
            (ExpressionType.PREFIX, ExpressionType.INFIX): self.prefix_to_infix,
            (ExpressionType.PREFIX, ExpressionType.PREFIX): lambda x: x,
            (ExpressionType.PREFIX, ExpressionType.POSTFIX): self.prefix_to_postfix,
            (ExpressionType.POSTFIX, ExpressionType.INFIX): self.postfix_to_infix,
            (ExpressionType.POSTFIX, ExpressionType.PREFIX): self.postfix_to_prefix,
            (ExpressionType.POSTFIX, ExpressionType.POSTFIX): lambda x: x,
        }

    def convert(self, expression, target_type):
        if not (converter := self._converters.get((expression.__type__, target_type))):
            raise ValueError(f'Unsupported conversion from {expression.type} to {target_type.name.lower()}')
        return converter(expression)

    def infix_to_prefix(self, expression: InfixExpression):
        return self.postfix_to_prefix(
            self.infix_to_postfix(expression)
        )

    def prefix_to_postfix(self, expression: PrefixExpression):
        return self.infix_to_postfix(
            self.prefix_to_infix(expression)
        )

    def postfix_to_infix(self, expression: PostfixExpression):
        return self.prefix_to_infix(
            self.postfix_to_prefix(expression)
        )

    @staticmethod
    def infix_to_postfix(expression: InfixExpression):
        result = []
        operators_stack = Stack()
        for token in expression.tokens:
            if token.type == TokenType.OPERAND:
                result.append(token)
            elif token.type == TokenType.VARIABLE:
                result.append(token)
            elif token.type == TokenType.CONSTANT:
                result.append(token)
            elif token.type == TokenType.FUNCTION:
                operators_stack.push(token)
            elif token.type == TokenType.OPERATOR:
                while operators_stack:
                    if (
                        token.priority < operators_stack.top().priority
                        or (
                            token.priority == operators_stack.top().priority
                            and not token.unary
                        )
                    ):
                        result.append(operators_stack.pop())
                    else:
                        break
                operators_stack.push(token)
            elif token.type == TokenType.BRACKET:
                if token.value == '(':
                    operators_stack.push(token)
                elif token.value == ')':
                    while operators_stack.top().value != '(' and not operators_stack.empty():
                        result.append(operators_stack.pop())
                    operators_stack.pop()
                    if operators_stack and operators_stack.top().type == TokenType.FUNCTION:
                        result.append(operators_stack.pop())
        while operators_stack:
            result.append(operators_stack.pop())

        expr = PostfixExpression.from_tokens(result)
        expr.set_variables(**expression.variables)
        return expr

    @staticmethod
    def prefix_to_infix(expression: PrefixExpression):
        stack = Stack()
        for token in expression.tokens[::-1]:
            if token.type == TokenType.OPERAND:
                stack.push([token])
            elif token.type == TokenType.VARIABLE:
                stack.push([token])
            elif token.type == TokenType.CONSTANT:
                stack.push([token])
            elif token.type == TokenType.OPERATOR:
                left_operand = stack.pop() if not token.unary else None
                right_operand = stack.pop()
                x = [brackets.get_token('(')]
                if left_operand:
                    x.extend(left_operand)
                x.append(token)
                x.extend(right_operand)
                x.append(brackets.get_token(')'))
                stack.push(x)
            elif token.type == TokenType.FUNCTION:
                operand = stack.pop()
                x = [token, brackets.get_token('(')]
                x.extend(operand)
                x.append(brackets.get_token(')'))
                stack.push(x)
            elif token.type == TokenType.BRACKET:
                raise InvalidExpressionError('PostfixExpression should not have brackets')

        result = stack.pop()

        expr = InfixExpression.from_tokens(result)
        expr.set_variables(**expression.variables)
        return expr

    @staticmethod
    def postfix_to_prefix(expression: PostfixExpression):
        stack = Stack()
        for token in expression.tokens:
            if token.type == TokenType.OPERAND:
                stack.push([token])
            elif token.type == TokenType.VARIABLE:
                stack.push([token])
            elif token.type == TokenType.CONSTANT:
                stack.push([token])
            elif token.type == TokenType.OPERATOR:
                left_operand = stack.pop()
                right_operand = stack.pop() if not token.unary else None
                x = [token]
                if right_operand:
                    x.extend(right_operand)
                x.extend(left_operand)
                stack.push(x)
            elif token.type == TokenType.FUNCTION:
                operand = stack.pop()
                x = [token]
                x.extend(operand)
                stack.push(x)
            elif token.type == TokenType.BRACKET:
                raise InvalidExpressionError('PostfixExpression should not have brackets')

        result = stack.pop()

        expr = PrefixExpression.from_tokens(result)
        expr.set_variables(**expression.variables)
        return expr


_converter = Converter()


def to_postfix(expression: BaseExpression):
    global _converter
    return _converter.convert(expression, ExpressionType.POSTFIX)


def to_prefix(expression: BaseExpression):
    global _converter
    return _converter.convert(expression, ExpressionType.PREFIX)


def to_infix(expression: BaseExpression):
    global _converter
    return _converter.convert(expression, ExpressionType.INFIX)