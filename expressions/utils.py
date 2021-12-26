from typing import Optional

from expressions import BaseExpression, InfixExpression, PrefixExpression, PostfixExpression


def get_expression(expression_string) -> Optional[BaseExpression]:
    try:
        return InfixExpression(expression_string)
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
