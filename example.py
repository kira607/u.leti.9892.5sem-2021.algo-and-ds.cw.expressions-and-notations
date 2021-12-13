from expressions import BaseExpression, SimpleExpression
from expressions.slib import Stack


def main():
    x = 10  # noqa
    from math import e, cos, log, sin, pi  # noqa
    exp = '1         + 2*e^x - (10 * 2 ^ cos(4*x)       -ln(4)*abs(log(sin(522.44-pi*2))))'
    exp2 = '1         + 2*e^x - (10 * 2 ^ (4*x)       -4*522.44-pi*2)'
    print(eval(exp.replace('^', '**').replace('ln', 'log')))  # 44047.933931765
    print(eval(exp2.replace('^', '**').replace('ln', 'log')))  # 44047.933931765
    tokens = BaseExpression.tokenize(exp)
    print(tokens)
    for token in tokens:
        print(token, end=' ')
    s = SimpleExpression(exp2)
    print()
    print(s.validated)
    s.set_variables(x=10)
    print(s.value)
    for c in s.validated:
        print(c, end=' ')
    print()


if __name__ == '__main__':
    main()
