import re

class TextAnalyzer(object):
    @staticmethod
    def sentences(text: str):
        punctuators = re.split(r'[.!?]+(?=\s+|$)', text)
        punctuators.pop()
        return punctuators

    @staticmethod
    def count_of_every_sentence_type(text: str):
        punctuators = ('.', '?', '!')
        return tuple(len(re.findall(fr'[{p}]+(?=\s+|$)', text)) for p in punctuators)

    @staticmethod
    def average_sentence_length(text: str):
        sentences = TextAnalyzer.sentences(text)

        for sentence in sentences:
            words = TextAnalyzer.get_words(sentence)
            yield round(sum(map(len, words)) / len(words), 2)

    @staticmethod
    def get_words(text: str):
        return re.findall(r'\b[а-яА-Я]+\b', text)

    @staticmethod
    def find_words_with_same_vowel_and_consonant(text: str):
        words = re.finditer(r'\b[а-яА-Я]+\b', text)

        vowels = "аеёиоуыэюяАЕЁИОУЫЭЮЯ"
        consonants = "бвгджзйклмнпрстфхцчшщБВГДЖЗЙКЛМНПРСТФХЦЧШЩ"

        for word in words:
            if len(re.findall(fr'[{vowels}]', word[0])) == len(re.findall(fr'[{consonants}]', word[0])):
                yield word[0], word.start()

    @staticmethod
    def get_words_with_len(text: str, length: int):
        return re.findall(fr'\b[а-яА-Я]{{{length}}}\b', text)

    @staticmethod
    def get_smileys(text: str):
        return re.findall(r'((?<=\s)[:;]-*([()\[\]])\2*(?=\s+))', text)

    @staticmethod
    def get_hex_numbers(text: str):
        return re.findall(r'\b[-+]?0[xXхХ][0-9a-fA-F]+\b', text)

    @staticmethod
    def plus_after_digit_count(text: str):
        return re.findall(r'(?<=[(\s])[-+]?\d+(?:\.\d*)?[ \t]*\+', text)
