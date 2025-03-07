from validators import validate_ln_calc_input
from math import log


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


# In case if eps is the difference between math.log and result:
# def find_n_for_series(epsilon: float, value: float) -> tuple[float, int]:
#     """Approximates ln(value) using Taylor series expansion.
#
#     :param epsilon: float, Required precision (acceptable error threshold).
#     :param value: float, Input value for natural logarithm calculation.
#     :return: Tuple containing (approximation result, terms used).
#     """
#     result = 0
#     math_result = log(value)
#     num_of_members = 1
#
#     for num_of_members in range(1, 501):
#         result = calc_ln_using_taylor_series(value, num_of_members)
#         if abs(result - math_result) < epsilon:
#             return result, num_of_members
#
#     return result, num_of_members


def calculate_natural_nums(numbers: list) -> tuple:
    return tuple(filter(lambda x: x > 0, numbers))


def calculate_sum_of_odd_indexed_elements(numbers: tuple | list) -> float | None:
    return sum(numbers[1::2]) if len(numbers) >= 2 else None


def calculate_sum_of_elements_between_negative_elements(numbers: tuple | list) -> float | None:
    negative_elements = tuple(filter(lambda x: x < 0, numbers))

    if len(negative_elements) <= 1:
        return None

    first_index = numbers.index(negative_elements[0])
    second_index = len(numbers) - numbers[::-1].index(negative_elements[-1]) - 1

    return None if abs(first_index - second_index) <= 1 else sum(numbers[first_index + 1:second_index])
