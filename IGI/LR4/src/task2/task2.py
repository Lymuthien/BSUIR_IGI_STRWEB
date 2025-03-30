import os
import re
import zipfile


class FileManager(object):
    @staticmethod
    def load(filename: str):
        with open(filename, 'r', encoding='utf-8') as f:
            return f.read()

    @staticmethod
    def save(data, filename: str):
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(data)


class ZipManager(object):
    @staticmethod
    def save(filename: str, archive_name: str):
        with zipfile.ZipFile(archive_name, 'w', zipfile.ZIP_DEFLATED) as zf:
            zf.write(filename, arcname=os.path.basename(filename))

    @staticmethod
    def load(archive_name: str, filename: str):
        with zipfile.ZipFile(archive_name, 'r', zipfile.ZIP_DEFLATED) as zf:
            with zf.open(filename) as file:
                return file.read().decode("utf-8")

    @staticmethod
    def file_info(archive_name: str, filename: str):
        with zipfile.ZipFile(archive_name, 'r', zipfile.ZIP_DEFLATED) as zf:
            return zf.getinfo(filename)


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


class Task2(object):
    def __init__(self):
        self._text = FileManager.load('../../data/text.txt')
        self._string_handler = TextAnalyzer()
        self._final_text = ''

    def run(self):
        self._calculate_results()

        FileManager.save(self._final_text, '../../data/final_text.txt')
        ZipManager.save('../../data/final_text.txt', '../../data/final_text.zip')

        text = ZipManager.load('../../data/final_text.zip', 'final_text.txt')
        print(f'Текст из архива:\n{text}')

        info = ZipManager.file_info('../../data/final_text.zip', 'final_text.txt')
        print(f'Информация о файле в архиве:\n{self._file_info(info)}')

    def _calculate_results(self):
        sentence_count = len(self._string_handler.sentences(self._text))
        every_sentences_count = self._string_handler.count_of_every_sentence_type(self._text)
        average_word_length_in_sentence = tuple(self._string_handler.average_sentence_length(self._text))
        average_word_length_in_text = round(sum(average_word_length_in_sentence) / sentence_count, 2)
        smileys_count = len(self._string_handler.get_smileys(self._text))
        hex_count = len(self._string_handler.get_hex_numbers(self._text))
        plus_after_digit_count = len(self._string_handler.plus_after_digit_count(self._text))
        all_words_len_4 = len(self._string_handler.get_words_with_len(self._text, 4))
        words = tuple(self._string_handler.find_words_with_same_vowel_and_consonant(self._text))
        sorted_words = sorted(self._string_handler.get_words(self._text), key=len, reverse=True)

        self._final_text += f'Количество предложений в тексте: {sentence_count}\n' + \
                            f'Количество повествовательных, вопросительных, побудительных предложений: ' + \
                            f'{every_sentences_count}\n' + \
                            f'Средняя длина предложения в символах: {average_word_length_in_sentence}\n' + \
                            f'Средняя длина слова в тексте в символах: {average_word_length_in_text}\n' + \
                            f'Количество смайликов: {smileys_count}\n' + \
                            f'Количество шестнадцатеричных цифр: {hex_count}\n' + \
                            f'Количество цифр d +: {plus_after_digit_count}\n' + \
                            f'Слова длиной 4: {all_words_len_4}\n' + \
                            f'Слова, у которых число гласных равно числу согласных и позиция:\n{words}\n' + \
                            f'Слова в порядке убывания длин:\n{sorted_words}\n'

    def _file_info(self, info: zipfile.ZipInfo):
        return (f'Исходный размер: {info.file_size} байт. '
                f'\nСжатый размер: {info.compress_size} байт')


if __name__ == '__main__':
    task2 = Task2()
    task2.run()
