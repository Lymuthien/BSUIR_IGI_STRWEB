import math
from mathematics import find_n_for_series, calculate_natural_nums
from utils import repeating_program, init_with_validating_user_input, init_with_random
from io_functions import input_with_validating
from validators import validate_octal_string


@repeating_program
def task1():
    x = float(input_with_validating(lambda i: abs(float(i)) < 1 and float(i) != 0,
                                    'Enter the value of x: (-1; 0) or (0; 1): '))
    eps = float(input_with_validating(lambda i: float(i) > 0, 'Enter the value of eps: (0, +inf): '))
    n, f_x = find_n_for_series(eps, x)
    result_lst = (x, n, f_x, math.log(x + 1), eps)

    print(*result_lst)


@repeating_program
def task2():
    numbers = []
    generating_way = int(input_with_validating(lambda i: 0 <= int(i) <= 1, '0 - Generate sequence, 1 - Input: '))

    if generating_way == 0:
        init_with_random(numbers, max_iterations=100)
    else:
        init_with_validating_user_input(numbers, int, int, 'Enter integer number (0 to stop):', 0)

    print('Orig numbers: ', *numbers)
    print(f'Count of numbers: {len(numbers)}. Count of natural numbers: {len(calculate_natural_nums(numbers))}')


@repeating_program
def task3():
    string = input('Enter string: ')
    print(['It is not octal number.', 'It is octal number.'][validate_octal_string(string)])



if __name__ == '__main__':
    task3()

