from expressions import get_expression, to_infix, to_prefix, to_postfix
from expressions.token import functions


def main():
    while True:
        print('-'*120)
        print('If you want to exit input empty string')
        print(f'Available math functions: {", ".join(functions)}')
        expression_string = input('Input expression (in any notation): ')

        if expression_string == '':
            print('Bye')
            break

        if not (expression := get_expression(expression_string)):
            print('Given string is not an expression or given expression is invalid')
            continue

        print(f'Your expression({expression.type}): {expression}\n')

        # Variables

        variables = {}

        if len(tuple(expression.variables_names())) > 0:
            for var in expression.variables_names():
                while True:
                    try:
                        variables[var] = float(input(f'Input variable {var}: '))
                        break
                    except ValueError:
                        print('Variable must be a real number')

        expression.set_variables(**variables)
        print()

        # Conversion and evaluation

        print(f'Evaluation: ')

        infix = to_infix(expression)
        print(f'Infix: {infix} = {infix.value}')

        prefix = to_prefix(expression)
        print(f'Prefix {prefix} = {prefix.value}')

        postfix = to_postfix(expression)
        print(f'Postfix: {postfix} = {postfix.value}')

        print()


if __name__ == '__main__':
    main()
