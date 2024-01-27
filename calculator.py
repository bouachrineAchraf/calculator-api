def calculate_npi(expression):
    stack = []
    operators = {'+': lambda x, y: x + y, '-': lambda x, y: x - y, '*': lambda x, y: x * y, '/': lambda x, y: x / y}

    tokens = expression.split()

    for token in tokens:
        if token.isdigit() or (token[0] == '-' and token[1:].isdigit()):
            stack.append(float(token))
        elif token in operators:
            if len(stack) < 2:
                raise ValueError("Not enough operands for operator {}".format(token))
            operand2 = stack.pop()
            operand1 = stack.pop()
            result = operators[token](operand1, operand2)
            stack.append(result)
        else:
            raise ValueError("Invalid token: {}".format(token))

    if len(stack) != 1:
        raise ValueError("Invalid expression")

    return stack[0]
