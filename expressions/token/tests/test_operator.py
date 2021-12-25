from expressions.token import operators


def test_operators():
    for op in ('+', '-', '*', '/', '^'):
        assert op in operators
