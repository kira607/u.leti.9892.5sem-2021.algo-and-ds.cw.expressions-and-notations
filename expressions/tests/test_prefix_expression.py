import pytest

from expressions import PrefixExpression
from expressions.errors import InvalidExpressionError


@pytest.mark.parametrize(
    'expression, variables, expected_value',
    (
        ('- 4 x', {'x': 10}, -6),
        ('abs - pi x', {'x': 220}, 216.85840734641022),
        ('f', {'f': 2}, 2)
    )
)
def test_prefix_expression(expression, variables, expected_value):
    e = PrefixExpression(expression)
    e.set_variables(**variables)
    assert e.value == expected_value


@pytest.mark.parametrize(
    'expression, variables, exception',
    (
        ('', {}, InvalidExpressionError),
        ('(1))', {}, InvalidExpressionError),
        ('((1)', {}, InvalidExpressionError),
        ('))', {}, InvalidExpressionError),
        ('0100', {}, InvalidExpressionError),
        ('log(14+2,, 1+1)', {}, InvalidExpressionError),
        ('-+/3', {}, InvalidExpressionError),
        ('1-x4', {'x': 34}, InvalidExpressionError),
        ('1-A///4', {'A': 8}, InvalidExpressionError),
        ('/1-A//4', {'A': 8}, InvalidExpressionError),
        ('1-A//4+', {'A': 8}, InvalidExpressionError),
        ('1-A/,/4+', {'A': 8}, InvalidExpressionError),
    ),
)
def test_prefix_expression_with_exception(expression, variables, exception):
    with pytest.raises(exception):
        e = PrefixExpression(expression)
        e.set_variables(**variables)
        _ = e.value
