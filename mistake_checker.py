from spellchecker import SpellChecker
from global_methods import get_text_from_file, load_yaml_config, remove_punctuation


class MistakeChecker:
    def __init__(self):
        self.spell = SpellChecker()
        return

    def check_if_mistake(self, string_input='something is happening here'):
        # remove punctuation
        parsed_string_input = remove_punctuation(string_input)

        # spellcheck
        # if mistake, adjust for basic spelling
        
        # spellcheck

        word_array = parsed_string_input.split()
        misspelled = self.spell.unknown(word_array)
        print(misspelled)
        if len(misspelled) > 0:
            return True
        else:
            return False
    
    def add_spaces(concatenated_text, word_list):
        # Initialize an empty list to hold the words
        words = []
        i = 0
        while i < len(concatenated_text):
            for word in word_list:
                # Check if the word matches the current position in the concatenated text
                if concatenated_text.startswith(word, i):
                    words.append(word)
                    i += len(word)
                    break
            else:
                # If no word matches, just move to the next character
                i += 1

        # Join the words with spaces
        spaced_text = ' '.join(words)
        return spaced_text

    # Example usage
    concatenated_text = "seenartificialintelligenceis"
    word_list = ["seen", "artificial", "intelligence", "is"]
    spaced_text = add_spaces(concatenated_text, word_list)
    print(spaced_text)


    def correct_mistake(self, string_input='something is happening here'):
        word_array = string_input.split()
        misspelled = self.spell.unknown(word_array)
        
        for word in misspelled:
            # Get the one `most likely` answer
            print(self.spell.correction(word))

            # Get a list of `likely` options
            print(self.spell.candidates(word))
        
        return

