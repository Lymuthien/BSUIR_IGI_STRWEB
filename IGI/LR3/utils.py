from io_functions import ask_for_repeat


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