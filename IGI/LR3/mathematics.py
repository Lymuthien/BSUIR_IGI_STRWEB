from validators import validate_any_input, validate_ln_calc_input


def calc_ln_using_taylor_series(x: float, n: int) -> float:
    """Calculates the ln of the argument x + 1 for a given number of terms of the taylor series.

    :param x: float, Value in (-1; 1).
    :param n: int, Number of terms of the taylor series, in [1; +inf].
    :return: float, The sum of the terms of the taylor series.
    """
    validate_ln_calc_input(x, n)
    return sum(pow(-1, i - 1) * pow(x, i) / i for i in range(1, n + 1))


def find_n_for_series(epsilon: float, value: float) -> tuple[float, int]:
    """Approximates ln(value) using Taylor series expansion.

    :param epsilon: float, Required precision (acceptable error threshold).
    :param value: float, Input value for natural logarithm calculation.
    :return: Tuple containing (approximation result, terms used).
    """
    old_result = calc_ln_using_taylor_series(value, 1)
    result = 0.1
    num_of_members = 1

    for num_of_members in range(2, 501):
        result = calc_ln_using_taylor_series(value, num_of_members)
        if abs(result - old_result) < epsilon:
            return result, num_of_members

    return result, num_of_members
