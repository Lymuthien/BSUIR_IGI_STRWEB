def validate_ln_calc_input(value: float, n: int) -> None:
    """
    Validates input parameters for logarithm calculation function.

    :param value: X argument for ln(1+x) calculation.
    :param n: Number of Taylor series terms to use.
    :raises ValueError:
        If either:
            - Absolute value of 'value' is >= 1
            - 'n' parameter is less than 1
    """
    if abs(value) >= 1 or n < 1:
        raise ValueError


def validate_any_input(value, validator: callable) -> bool:
    """
    Validates a user-provided value using a specified validator function.

    :param value: Value to validate.
    :param validator: The validator function to use.
    :return: True if the value passes validation, False otherwise.
    """
    try:
        result = validator(value)
        if isinstance(result, bool):
            return result
        return True
    except Exception:
        return False


# Could use the previous function instead of this, but the task requires that specific exception classes be handled.
def validate_octal_string(string: str) -> bool:
    """
    Validates if a string represents a valid octal number.

    Checks if the string can be converted to base-8 integer using int().
    Does not allow:
        - Any characters outside 0-7 range.
        - Any letters except python's octal prefixes (0o, 0O) at the beginning.
        - Empty strings.

    :param string: Input to validate as octal representation.
    :return: True if valid octal number, False otherwise.
    """
    try:
        int(string, 8)
        return True
    except ValueError:
        return False
