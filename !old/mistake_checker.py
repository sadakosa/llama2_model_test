from spellchecker import SpellChecker
import csv
import string


class MistakeChecker:
    def __init__(self):
        self.spell = SpellChecker()
        self.word_list = self.__get_word_list()
        return

    def check_if_mistake(self, text='something is happening here'):
        # prepare text
        parsed_text = self.__remove_punctuation(text)
        word_array = parsed_text.split()

        # spellcheck
        misspelled = self.spell.unknown(word_array)
        print(misspelled)

        if len(misspelled) > 0:
            return True
        else:
            return False

    # def correct_if_mistake(self, text='something is happening here'):
    #     # if mistake, adjust for basic spelling
    #     is_mistake = self.check_if_mistake(text)
    #     if is_mistake:
    #         # google did you mean
    #         # check if still mispelled
    #         # if yes, return yes to direct it to groq
    #     else:
    #         return text

    # ================== PRIVATE METHODS ==================
    def __remove_punctuation(self, text):
        return ''.join([char for char in text if char not in string.punctuation])

    def __get_word_list(self):
        csv_file_path = 'resources/word_list.csv'
        word_list = []

        with open(csv_file_path, mode='r') as file: # open the csv file, read
            csv_reader = csv.reader(file)
            
            for row in csv_reader:
                word_list.append(row)
        return word_list



