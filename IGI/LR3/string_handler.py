def find_words_with_odd_count_of_letters(string_sequence: list | tuple) -> tuple:
    """
    Filters words with odd character count from input sequence.

    :param string_sequence: Sequence of words to process.
    :return: Tuple containing only words with odd length (1, 3, 5... characters).
    """
    return tuple(filter(lambda word: len(word) % 2 == 1, string_sequence))


def find_shortest_word(string_sequence: list | tuple, begin: str = None) -> tuple | None:
    """
    Finds the shortest word in sequence, optionally filtered by starting character.

    :param string_sequence: Sequence of words to search.
    :param begin: Optional starting character filter (default: None)
    :return: Shortest matching word as list. Returns None if no words match the criteria.
    """
    if begin:
        words = filter(lambda word: word[0] == 'i', string_sequence)
    else:
        words = string_sequence.copy()
    sorted_words = tuple(sorted(words, key=len))

    return sorted_words[0] if len(sorted_words) else None


def find_repeating_words(string_sequence: list | tuple) -> tuple:
    """
    Identifies words that are repeated in input sequence.

    :param string_sequence: Sequence of words to analyze.
    :return: Tuple of unique words that occur multiple times.
    """
    return tuple(set(filter(lambda word: string_sequence.count(word) >= 2, string_sequence)))
