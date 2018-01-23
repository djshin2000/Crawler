
def check_palindrome(input_string):
    # cycle = 0
    if len(input_string) % 2 == 0:
        cycle = len(input_string) / 2
    else:
        cycle = (len(input_string) / 2) - 0.5

    last_idx = len(input_string) - 1
    result = True
    for i in range(int(cycle)):
        print(input_string[i], input_string[last_idx])
        if input_string[i] != input_string[last_idx]:
            result = False
        last_idx -= 1
    return result


check_palindrome('abacaba')
