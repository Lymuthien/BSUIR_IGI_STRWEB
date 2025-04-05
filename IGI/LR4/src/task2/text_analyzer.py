import re


class TextAnalyzer(object):
    """Provides methods for analyzing text. Includes functionality to process sentences."""

    @staticmethod
    def sentences(text: str):
        """
        Splits the text into sentences using punctuation marks as delimiters (.!?).

        :param text: The input text to split into sentences.
        :return: A list of sentences after splitting based on punctuation.
        """

        punctuators = re.split(r'[.!?]+(?=\s+|$)', text)
        punctuators.pop()
        return punctuators

    @staticmethod
    def count_of_every_sentence_type(text: str):
        """
        Calculates the count of sentences ending with '.', '!', or '?'.

        :param text: The input text to analyze.
        :return: A tuple containing counts of sentences ending with '.', '?', and '!' respectively.
        """

        punctuators = ('.', '?', '!')
        return tuple(len(re.findall(fr'[{p}]+(?=\s+|$)', text)) for p in punctuators)

    @staticmethod
    def average_sentence_length(text: str):
        """
        Calculates the average word length in each sentence of the text.

        :param text: The input text to analyze.
        :yield: The average word length of each sentence, rounded to 2 decimal places.
        """

        sentences = TextAnalyzer.sentences(text)

        for sentence in sentences:
            words = TextAnalyzer.get_words(sentence)
            yield round(sum(map(len, words)) / len(words), 2)

    @staticmethod
    def get_words(text: str):
        """
        Extracts all words from the text using a regular expression.

        :param text: The input text to extract words from.
        :return: A list of words found in the text (Cyrillic-based words).
        """

        return re.findall(r'\b[а-яА-Я]+\b', text)

    @staticmethod
    def find_words_with_same_vowel_and_consonant(text: str):
        """
        Finds words where the number of vowels equals the number of consonants
        and returns their positions in the text.

        :param text: The input text to analyze.
        :yield: A tuple with the word and its starting position in the text.
        """

        words = re.finditer(r'\b[а-яА-Я]+\b', text)

        vowels = "аеёиоуыэюяАЕЁИОУЫЭЮЯ"
        consonants = "бвгджзйклмнпрстфхцчшщБВГДЖЗЙКЛМНПРСТФХЦЧШЩ"

        for word in words:
            if len(re.findall(fr'[{vowels}]', word[0])) == len(re.findall(fr'[{consonants}]', word[0])):
                yield word[0], word.start()

    @staticmethod
    def get_words_with_len(text: str, length: int):
        """
        Finds all words in the text that have a specific length.

        :param text: The input text to analyze.
        :param length: The length of words to extract.
        :return: A list of words with the specified length.
        """

        return re.findall(fr'\b[а-яА-Я]{{{length}}}\b', text)

    @staticmethod
    def get_smileys(text: str):
        """
        Extracts smileys (e.g., :), ;-), ;]) from the text.

        :param text: The input text to analyze.
        :return: A list of tuples, where each tuple contains the smiley and the repetition symbol.
        """

        return re.findall(r'((?<=\s)[:;]-*([()\[\]])\2*(?=\s+))', text)

    @staticmethod
    def get_hex_numbers(text: str):
        """
        Extracts hexadecimal numbers from the text.

        :param text: The input text to analyze.
        :return: A list of hexadecimal numbers found in the text.
        """

        return re.findall(r'\b[-+]?0[xXхХ][0-9a-fA-F]+\b', text)

    @staticmethod
    def plus_after_digit_count(text: str):
        """
        Finds all numbers in the text that are immediately followed by a '+' symbol.

        :param text: The input text to analyze.
        :return: A list of matches for numbers that have a '+' directly after them.
        """

        return re.findall(r'(?<=[(\s])[-+]?\d+(?:\.\d*)?[ \t]*\+', text)
