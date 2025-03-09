import random

from io_functions import ask_for_repeat, input_with_validating


def repeating_program(foo: callable) -> callable:
    """
    Decorator that repeats the wrapped function execution until user declines.

    :param foo: Function to be repeated (should accept no arguments).
    :return: Wrapped function with repeat logic.
    """

    def wrapper():
        while True:
            foo()
            if not ask_for_repeat():
                break

    return wrapper


def generate_int_sequence(mid: int = 0, spread=100):
    """
    Generates an infinite sequence of random integers within a specified range.

    :param mid: Central value defining the middle of the range (default 0).
    :param spread: Maximum deviation from mid in both directions (default 100).
    :yield: Integers randomly chosen from [mid-spread, mid+spread] range.
    """
    while True:
        yield random.randint(mid - spread, mid + spread)


def init_with_random(sequence: list, stop: int = 0, max_iterations: int = 100) -> None:
    """
    Populates a list with random integers until stop value or iteration limit is reached.

    :param sequence: Target list to populate with numbers.
    :param stop: Value that stops generation when encountered (default 0).
    :param max_iterations: Safety limit to prevent infinite loops (default 100).
    """
    iterations = 0

    for num in generate_int_sequence(mid=stop):
        iterations += 1
        if num == stop or iterations == max_iterations:
            sequence.append(stop)
            break
        sequence.append(num)


def init_with_validating_user_input(sequence: list, validator: callable, transformation: callable = str,
                                    msg: str = '', stop: int = 0):
    """
    Populates a list with user input validated through provided functions until stop value.

    After validating input using validator function, it's converted with transformation function.
    Then result is appended to list. Cycle repeat until transformed input matches stop value.

    :param sequence: Target list to populate with processed inputs.
    :param validator: Validation function that accepts raw input string and returns bool.
    :param transformation: Conversion function for validated input (default str).
    :param msg: Custom prompt message for input requests (default empty).
    :param stop: Value that stops collection when matched post-transformation (default 0).
    """
    number = -1

    while number != stop:
        number = transformation(input_with_validating(validator, msg))
        sequence.append(number)
