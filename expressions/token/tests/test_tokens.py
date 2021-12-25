import pytest

from expressions.token import Token, TokenType, Operator


def test_token___init__():
    x = Token(None)
    assert x.type == TokenType.NONE


@pytest.mark.parametrize('data', (1, '1', {1: 1}, [1, 1]))
def test_token___init___with_exception(data):
    with pytest.raises(TypeError):
        Token(data)


def test_operator___init__():
    op = Operator('+')


def test_operator___init___with_exception():
    with pytest.raises(ValueError):
        Operator('x')
