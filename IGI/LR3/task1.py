import math
from mathematics import calc_ln_using_taylor_series, find_n_for_series
from io_functions import input_with_validating
from utils import repeating_program


@repeating_program
def main():
    x = float(input_with_validating(lambda i: abs(float(i)) < 1, 'Enter the value of x: (-1; 1): '))
    eps = float(input_with_validating(lambda i: float(i) > 0, 'Enter the value of eps: (0, +inf): '))
    n, f_x = find_n_for_series(eps, x)
    result_lst = (x, n, f_x, math.log(x + 1), eps)
    print(*result_lst)


if __name__ == '__main__':
    main()
