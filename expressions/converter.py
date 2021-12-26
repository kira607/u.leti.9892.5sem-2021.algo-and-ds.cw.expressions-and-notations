from expressions.base_expression import ExpressionType


class Converter:
    def __init__(self):
        self._converters = {
            (ExpressionType.SIMPLE, ExpressionType.SIMPLE): lambda x: x,
            (ExpressionType.SIMPLE, ExpressionType.PREFIX): self.simple_to_prefix,
            (ExpressionType.SIMPLE, ExpressionType.POSTFIX): self.simple_to_postfix,
            (ExpressionType.PREFIX, ExpressionType.SIMPLE): self.prefix_to_simple,
            (ExpressionType.PREFIX, ExpressionType.PREFIX): lambda x: x,
            (ExpressionType.PREFIX, ExpressionType.POSTFIX): self.prefix_to_postfix,
            (ExpressionType.POSTFIX, ExpressionType.SIMPLE): self.postfix_to_simple,
            (ExpressionType.POSTFIX, ExpressionType.PREFIX): self.postfix_to_prefix,
            (ExpressionType.POSTFIX, ExpressionType.POSTFIX): lambda x: x,
        }

    def convert(self, expression, target_type):
        if not (converter := self._converters.get((expression.type, target_type))):
            raise ValueError(f'Unsupported conversion from {expression.type} to {target_type.name.lower()}')
        return converter(expression)

    def simple_to_prefix(self, expression):
        pass

    def simple_to_postfix(self, expression):
        pass

    def prefix_to_simple(self, expression):
        pass

    def prefix_to_postfix(self, expression):
        pass

    def postfix_to_simple(self, expression):
        pass

    def postfix_to_prefix(self, expression):
        pass
