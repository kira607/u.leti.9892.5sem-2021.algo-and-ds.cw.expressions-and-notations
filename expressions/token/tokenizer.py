from string import ascii_letters
from typing import List

from expressions.token_groups import functions, constants
from expressions.token_groups.operator import operators
from expressions.token.tokens import Token, Operator, Operand, Constant, Variable, Function, Bracket


class Tokenizer:
    def __init__(self):
        self.string = ''

    def tokenize(self, string: str) -> List[Token]:
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
                tokens.append(Operand(float(number)))
                number = ''

            if s in operators:
                tokens.append(Operator(s))
            elif s in '()':
                tokens.append(Bracket(s))
            elif function := self.get_function(i):
                tokens.append(Function(function))
                ignore = len(function) - 1
            elif constant := self.get_constant(i):
                tokens.append(Constant(constant))
                ignore = len(constant) - 1
            elif s in ascii_letters:
                tokens.append(Variable(s))
        if number:
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