import zipfile

from .file_managers import FileManager, ZipManager
from .text_analyzer import TextAnalyzer
from ..utils.utils import repeating_program


class Task2(object):
    """
    A class for processing a text file, analyzing its content, saving results to a file,
    archiving the file, and extracting information from the archive.
    """

    def __init__(self, filepath: str, archive_path: str):
        """
        Initializes the Task2 object with paths to the text file and archive.

        :param filepath: The path to save the processed result file.
        :param archive_path: The path to save the archive file.
        """

        self._text = FileManager.load('data/text.txt')
        self._string_handler = TextAnalyzer()
        self._final_text = ''
        self._file_path = filepath
        self._archive_name = archive_path

    @repeating_program
    def run(self):
        """
        Executes the main logic of the task:
        - Analyzes the text content.
        - Saves results to a file.
        - Archives the file.
        - Extracts and prints file content and archive information.
        """

        self._calculate_results()

        FileManager.save(self._final_text, self._file_path)
        ZipManager.save(self._file_path, self._archive_name)

        text = ZipManager.load(self._archive_name, self._file_path.split('/')[-1])
        print(f'Text from archive:\n{text}')

        info = ZipManager.file_info(self._archive_name, self._file_path.split('/')[-1])
        print(f'Information about file:\n{self._file_info(info)}')

    def _calculate_results(self):
        """
        Analyzes the text to calculate various statistics, such as:
        - Number of sentences.
        - Count of different types of sentences.
        - Average word and sentence lengths.
        - Number of smileys, hexadecimal numbers, words of specific length, etc.

        The results are formatted into a string and saved in the `_final_text` attribute.
        """

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

        self._final_text += f'Number of sentences in the text: {sentence_count}\n' + \
                            f'Number of declarative, interrogative, and exclamatory sentences: ' + \
                            f'{every_sentences_count}\n' + \
                            f'Average sentence length in characters: {average_word_length_in_sentence}\n' + \
                            f'Average word length in the text in characters: {average_word_length_in_text}\n' + \
                            f'Number of smileys: {smileys_count}\n' + \
                            f'Number of hexadecimal numbers: {hex_count}\n' + \
                            f'Number of digits followed by "+": {plus_after_digit_count}\n' + \
                            f'Words with a length of 4: {all_words_len_4}\n' + \
                            f'Words in which the number of vowels equals the number of consonants and their positions:\n{words}\n' + \
                            f'Words sorted in descending order of length:\n{sorted_words}\n'

    @staticmethod
    def _file_info(info: zipfile.ZipInfo):
        """
        Formats information about a file within the archive.

        :param info: Information about a file within the archive, provided as a `ZipInfo` object.
        :return: A formatted string containing the original and compressed sizes of the file.
        """

        return (f'Original size: {info.file_size} bytes. '
                f'\nCompressed size: {info.compress_size} bytes')
