import pytest

from expressions import SimpleExpression
from expressions.errors import InvalidExpressionError


def python_eval(exp: str, variables: dict):
    from math import cos, log, sin, cos, sin, tan, log, log10, log2, sqrt, fabs, log10, factorial  # noqa
    from math import e, pi  # noqa

    def ctg(x):
        return cos(x) / sin(x)

    result = exp
    for k, v in variables.items():
        result = result.replace(k, f' {v} ')
    result = (
        result
        .replace('^', '**')
        .replace('ln', 'log')
        .replace('abs', 'fabs')
        .replace('lg', 'log10')
        .replace('fact', 'factorial')
    )
    return eval(result)


@pytest.mark.parametrize(
    'expression, variables',
    (
        ('1+2*e^x - (10 * 2 ^ cos(4*x)  -ln(4)*abs(lg(sin(522.44-pi*2))))', {'x': 10}),
        ('1  +- 2*e^x - (10 * 2 ^ (4*x)  -4*522.44-pi*2)', {'x': 10}),
        ('log2(14+2)', {}),
        ('+4 - (-1)', {}),
        ('+-+4 +(- (---1))', {}),
        ('----+--(-++-++-(-1))', {}),
        ('((-(((-(-1))))))', {}),
        ('(1)', {}),
        ('abs(-16)', {}),
        ('-00', {}),
    )
)
def test_simple_expression(expression, variables):
    s = SimpleExpression(expression)
    s.set_variables(**variables)
    assert s.value == python_eval(expression, variables)


@pytest.mark.parametrize(
    'expression, variables, exception',
    (
        ('1/0', {}, ZeroDivisionError),
        ('1/x', {'x': 0}, ZeroDivisionError),
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
        ('+ 3 4', {}, InvalidExpressionError),
    ),
)
def test_simple_expression_with_exception(expression, variables, exception):
    with pytest.raises(Exception):
        python_eval(expression, variables)
    with pytest.raises(exception):
        s = SimpleExpression(expression)
        s.set_variables(**variables)
        _ = s.value
