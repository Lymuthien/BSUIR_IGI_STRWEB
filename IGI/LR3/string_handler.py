def find_words_with_odd_count_of_letters(string_lst: list) -> list:
    return list(filter(lambda word: len(word) % 2 == 1, string_lst))


def find_shortest_word(string_lst: list, begin: str = None) -> list | None:
    if begin:
        words = filter(lambda word: word[0] == 'i', string_lst)
    else:
        words = string_lst.copy()
    sorted_words = list(sorted(words, key=len))
    return sorted_words[0] if len(sorted_words) else None


def find_repeating_words(string_lst: list) -> list:
    return list(set(filter(lambda word: string_lst.count(word) >= 2, string_lst)))
