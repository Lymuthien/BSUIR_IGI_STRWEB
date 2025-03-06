from validators import validate_any_input


def input_with_validating(validator: callable, msg: str = ''):
    """Performs validated input with retries on invalid data.

    :param validator: callable, Validation function (should return bool or raise exception for invalid input)
    :param msg: str, Input prompt message. Defaults to empty string.
    :return: Any, Validated input value.
    """
    while True:
        value = input(msg)
        if validate_any_input(value, validator):
            return value
        print('Invalid input. Try again.')


def ask_for_repeat() -> bool:
    """Asks a user to repeat.

    :return: bool: True if the answer is y, False otherwise.
    """
    choice = input("Repeat? (y/otherwise): ").lower()
    return True if choice == 'y' else False


