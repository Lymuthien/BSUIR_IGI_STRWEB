import random

from io_functions import ask_for_repeat, input_with_validating


def repeating_program(foo: callable):
    """Decorator that repeats the wrapped function execution until user declines.

    :param foo: Function to be repeated (should accept no arguments)
    :return: Wrapped function with repeat logic
    """

    def wrapper():
        while True:
            foo()
            if not ask_for_repeat():
                break

    return wrapper


def generate_int_sequence(mid: int = 0, spread=100):
    while True:
        yield random.randint(mid - spread, mid + spread)


def init_with_random(sequence: list, stop: int = 0, max_iterations: int = 100):
    iterations = 0

    for num in generate_int_sequence(mid=stop):
        iterations += 1
        if num == stop or iterations == max_iterations:
            sequence.append(stop)
            break
        sequence.append(num)


def init_with_validating_user_input(sequence: list, validator: callable, transformation: callable = str, msg: str = '', stop: int = 0):
    number = -1
    while number != stop:
        number = transformation(input_with_validating(validator, msg))
        sequence.append(number)
