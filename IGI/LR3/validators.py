def validate_ln_calc_input(value: float, n: int):
    """Checks the args for the logarithm calc function."""
    if abs(value) >= 1 or n < 1:
        raise ValueError


def validate_any_input(value, validator: callable) -> bool:
    """Validates a user-provided value using a specified validator function.

    :param value: Any, The value to validate.
    :param validator: callable, The validator function to use.
    :return: bool, True if the value passes validation, False otherwise."""
    try:
        result = validator(value)
        if isinstance(result, bool):
            return result
        return True
    except Exception:
        return False


# Could use the previous function instead of this, but the task requires that specific exception classes be handled
def validate_octal_string(string: str) -> bool:
    try:
        int(string, 8)
        return True
    except ValueError:
        return False
