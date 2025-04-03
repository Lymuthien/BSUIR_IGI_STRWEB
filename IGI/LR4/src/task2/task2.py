import zipfile

from .file_managers import FileManager, ZipManager
from .text_analyzer import TextAnalyzer
from ..utils.utils import repeating_program


class Task2(object):
    def __init__(self, filepath: str, archive_path: str):
        self._text = FileManager.load('data/text.txt')
        self._string_handler = TextAnalyzer()
        self._final_text = ''
        self._file_path = filepath
        self._archive_name = archive_path

    @repeating_program
    def run(self):
        self._calculate_results()

        FileManager.save(self._final_text, self._file_path)
        ZipManager.save(self._file_path, self._archive_name)

        text = ZipManager.load(self._archive_name, self._file_path.split('/')[-1])
        print(f'Текст из архива:\n{text}')

        info = ZipManager.file_info(self._archive_name, self._file_path.split('/')[-1])
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

    @staticmethod
    def _file_info(info: zipfile.ZipInfo):
        return (f'Исходный размер: {info.file_size} байт. '
                f'\nСжатый размер: {info.compress_size} байт')
