from expressions.token import Token, TokenType


class Delimiter(Token):
    __value_type__ = str
    __token_type__ = TokenType.DELIMITER

    def _check_value(self, value):
        if value != ',':
            raise ValueError('Delimiter must be a "," (comma)')
