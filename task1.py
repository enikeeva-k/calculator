def read_number(line, index):
    number = 0
    while index < len(line) and line[index].isdigit():
        number = number * 10 + int(line[index])
        index += 1
    if index < len(line) and line[index] == '.':
        index += 1
        decimal = 0.1
        while index < len(line) and line[index].isdigit():
            number += int(line[index]) * decimal
            decimal /= 10
            index += 1
    token = {'type': 'NUMBER', 'number': number}
    return token, index


def read_plus(line, index):
    token = {'type': 'PLUS'}
    return token, index + 1


def read_minus(line, index):
    token = {'type': 'MINUS'}
    return token, index + 1


def read_mul(line, index):
    token = {'type': 'MUL'}
    return token, index + 1


def read_div(line, index):
    token = {'type': 'DIV'}
    return token, index + 1


def tokenize(line, index=0):
    tokens = []
    while index < len(line):
        if line[index].isdigit():
            (token, index) = read_number(line, index)
        elif line[index] == '+':
            (token, index) = read_plus(line, index)
        elif line[index] == '-':
            (token, index) = read_minus(line, index)
        elif line[index] == '*':
            (token, index) = read_mul(line, index)
        elif line[index] == '/':
            (token, index) = read_div(line, index)
        elif line[index] == '(':
            # Found parentheses. Tokenize the contents.
            (nested_tokens, index) = tokenize(line, index + 1)
            token = {'type': 'EXPR', 'tokens': nested_tokens}
        elif line[index] == ')':
            index += 1
            # We finished tokenizing a parentheses. Break and return the tokens that we've collected so far.
            break
        else:
            print('Invalid character found: ' + line[index])
            exit(1)
        tokens.append(token)
    return tokens, index


def evaluate(tokens):
    if len(tokens) == 0:
        return 0

    # Replace expressions in parentheses with their resulting numbers.
    for x in range(len(tokens)):
        if tokens[x]['type'] == 'EXPR':
            expr_result = evaluate(tokens[x]['tokens'])
            tokens[x] = {'type': 'NUMBER', 'number': expr_result}

    # Create new list of tokens by calculating multiplications and divisions.
    # Initialize with the first number.
    tokens_after_mul_div = [tokens[0]]
    # Iterate through arithmetic signs.
    for x in range(1, len(tokens), 2):
        next_number = tokens[x + 1]['number']

        if tokens[x]['type'] == 'MUL':
            tokens_after_mul_div[-1]['number'] *= next_number
        elif tokens[x]['type'] == 'DIV':
            tokens_after_mul_div[-1]['number'] /= next_number
        else:
            # Leave plus and minus signs as is.
            tokens_after_mul_div.append(tokens[x])
            # The next number is also pushed into the list of tokens.
            tokens_after_mul_div.append(tokens[x + 1])

    # Calculate the final result.
    answer = tokens[0]['number']
    # Iterate through arithmetic signs.
    for x in range(1, len(tokens), 2):
        next_number = tokens[x + 1]['number']

        if tokens[x]['type'] == 'PLUS':
            answer += next_number
        elif tokens[x]['type'] == 'MINUS':
            answer -= next_number

    return answer


def test(line):
    (tokens, _index) = tokenize(line)
    actual_answer = evaluate(tokens)
    expected_answer = eval(line)
    if abs(actual_answer - expected_answer) < 1e-8:
        print("PASS! (%s = %f)" % (line, expected_answer))
    else:
        print("FAIL! (%s should be %f but was %f)" % (line, expected_answer, actual_answer))


# Add more tests to this function :)
def run_test():
    print("==== Test started! ====")
    test("15")
    test("1+2")
    test("1.0+2.1-3")

    test("2*5-1")
    test("1+1.5/2.0-3*2")

    test("(1+2)*(5*3)-(2/4)+(1)")
    test("(((((1)+1)+1)+1)+1)+1")

    print("==== Test finished! ====\n")


run_test()

while True:
    print('> ', end="")
    line = input()
    (tokens, _index) = tokenize(line)
    answer = evaluate(tokens)
    print("answer = %f\n" % answer)
