import math
from mathematics import find_n_for_series, calculate_natural_nums, calculate_sum_of_odd_indexed_elements, \
    calculate_sum_of_elements_between_negative_elements
from utils import repeating_program, init_with_validating_user_input, init_with_random
from io_functions import input_with_validating
from validators import validate_octal_string
from string_handler import find_words_with_odd_count_of_letters, find_shortest_word, find_repeating_words


@repeating_program
def task1():
    """
    Calculate the value of the function ln(1+x) using the expansion of the function into a
    taylor series with a given calculation accuracy.
    """
    x = float(input_with_validating(lambda i: abs(float(i)) < 1 and float(i) != 0,
                                    'Enter the value of x: (-1; 0) or (0; 1): '))
    eps = float(input_with_validating(lambda i: float(i) > 0, 'Enter the value of eps: (0, +inf): '))

    n, f_x = find_n_for_series(eps, x)
    result_lst = (x, n, f_x, math.log(x + 1), eps)

    print(*result_lst)


@repeating_program
def task2():
    """Calculate the number of natural numbers in the given sequence."""
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
    """Check if input string is an octal value."""
    string = input('Enter string: ')
    print('It is octal number.' if validate_octal_string(string) else 'It is not octal number.')


@repeating_program
def task4():
    """
    Analyze text and calculate various statistics.

    Determines:
    - Total word count.
    - Words with odd number of letters.
    - Shortest word starting with 'i'.
    - All repeating words.
    """
    string = ('So she was considering in her own mind, as well as she could, for the hot day made her feel very sleepy '
              'and stupid, whether the pleasure of making a daisy-chain would be worth the trouble of getting up and '
              'picking the daisies, when suddenly a White Rabbit with pink eyes ran close by her.')
    words = [word for el in string.lower().split(',') for word in el.strip().split()]

    word_count = len(words)
    words_with_odd_count_of_letters = find_words_with_odd_count_of_letters(words)
    shortest_word_with_first_i = find_shortest_word(words, 'i')
    repeating_words = find_repeating_words(words)

    print('Count of words:', word_count)
    print('Words with odd count of letters:', *words_with_odd_count_of_letters)
    print(f"Shortest word starting with 'i': {shortest_word_with_first_i or 'no word'}")
    print('Repeating words:', *repeating_words)


@repeating_program
def task5():
    """
    Find next values for a given sequence of float values:
    - Sum of elements with odd indexes.
    - Sum of elements between first and last negative elements.
    """
    numbers = input_with_validating(lambda s: tuple(map(float, s.strip().split())),
                                    'Enter the list (separated by space): ')
    numbers = tuple(map(float, numbers.strip().split()))

    sum_of_elements_with_odd_index = calculate_sum_of_odd_indexed_elements(numbers)
    sum_of_elements_between_first_last_negative = calculate_sum_of_elements_between_negative_elements(numbers)

    print('Sum of elements with odd index: ' +
          (f"{sum_of_elements_with_odd_index}"
          if sum_of_elements_with_odd_index is not None else 'no elements odd indexed'))
    print('Sum of elements between first and last negative: ' +
          (f"{sum_of_elements_between_first_last_negative}"
          if sum_of_elements_between_first_last_negative is not None
          else 'not enough negative elements or they are located nearby'))


def menu():
    tasks = {'1': task1, '2': task2, '3': task3, '4': task4, '5': task5}
    while True:
        choice = input('\nComplete task - 1..5'
                       '\nShow task condition - 1d..5d'
                       '\nExit - 0\n').strip()

        match choice:
            case cmd if cmd in tasks:
                tasks[cmd]()
            case cmd if cmd.endswith('d') and (num := cmd[:-1]) in tasks:
                print(tasks[num].__doc__)
            case '0':
                break
            case _:
                print('Invalid choice.')


if __name__ == '__main__':
    menu()
