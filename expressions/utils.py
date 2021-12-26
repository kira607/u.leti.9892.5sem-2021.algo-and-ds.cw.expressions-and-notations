from typing import Optional

from .base_expression import BaseExpression
from .infix_expression import InfixExpression
from .prefix_expression import PrefixExpression
from .postfix_expression import PostfixExpression


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
