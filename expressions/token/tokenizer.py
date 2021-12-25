from string import ascii_letters
from typing import List

from ._base import Token
from . import functions, constants, brackets, operators
from . import Delimiter, Operand, Variable
from ..errors import InvalidExpressionError


class Tokenizer:
    def __init__(self):
        self.string = ''

    def tokenize(self, string: str) -> List[Token]:
        '''
        Convert an expression string into a list of tokens

        :param string: expression
        :return: list of tokens
        '''
        self.string = string
        tokens = []
        number = ''
        ignore = 0
        for i in range(len(string)):
            if ignore:
                ignore -= 1 if ignore > 0 else 0
                continue

            s = string[i]

            if s in '1234567890.':
                number += s
            elif number:
                if number.startswith('0') and number.count('0') < len(number):
                    raise InvalidExpressionError('leading zeros in decimal integer literals are not permitted')
                tokens.append(Operand(float(number)))
                number = ''

            if s in operators:
                if s == '/' and string[i+1] == '/':
                    tokens.append(operators.get_token('//'))
                    ignore = 1
                    continue
                tokens.append(operators.get_token(s))
            elif s == ',':
                tokens.append(Delimiter(s, priority=-1))
            elif s in '()':
                tokens.append(brackets.get_token(s))
            elif function := self.get_function(i):
                tokens.append(functions.get_token(function))
                ignore = len(function) - 1
            elif constant := self.get_constant(i):
                tokens.append(constants.get_token(constant))
                ignore = len(constant) - 1
            elif s in ascii_letters:
                tokens.append(Variable(s))
        if number:
            if number.startswith('0') and number.count('0') < len(number):
                raise InvalidExpressionError('leading zeros in decimal integer literals are not permitted')
            tokens.append(Operand(float(number)))

        return tokens

    def get_function(self, index):
        for func in functions:
            if self.check_literal(func, index):
                return func

    def get_constant(self, index):
        for constant in constants:
            if self.check_literal(constant, index):
                return constant

    def check_literal(self, name, index):
        check = True
        for nxt, char in enumerate(name):
            try:
                if self.string[index+nxt] == char:
                    continue
                else:
                    check = False
                    break
            except IndexError:
                check = False
                break
        return check
