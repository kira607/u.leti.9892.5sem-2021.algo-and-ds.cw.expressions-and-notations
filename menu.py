from expressions import SimpleExpression, get_expression


def main():
    while True:
        print('-'*120)
        print('If you want to exit input empty string')
        expression_string = input('Input expression (in any notation): ')

        if expression_string == '':
            print('Bye')
            break

        if not (expression := get_expression(expression_string)):
            print('Given string is not an expression')
            continue

        print(f'Your expression({expression.type}): {expression}')


if __name__ == '__main__':
    main()
