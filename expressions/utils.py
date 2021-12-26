from typing import Optional

from expressions import BaseExpression, SimpleExpression, PrefixExpression, PostfixExpression


def get_expression(expression_string) -> Optional[BaseExpression]:
    try:
        return SimpleExpression(expression_string)
    except Exception:
        pass

    try:
        return PrefixExpression(expression_string)
    except Exception:
        pass

    try:
        return PostfixExpression(expression_string)
    except Exception:
        pass

    return None
