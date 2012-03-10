import re
import string

from nltk import tokenize

import words

class colors:
    """
    Used to highlight text when printing to shell
    ex) print colors.WARNING + "Warning" + colors.ENDC
    """

    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

    def disable(self):
        self.HEADER = ''
        self.OKBLUE = ''
        self.OKGREEN = ''
        self.WARNING = ''
        self.FAIL = ''
        self.ENDC = ''


class Engrish(object):

    def __init__(self, document):
        """
        Takes a document, turns into text stream, splits into sentences
        """
        self.colors = colors()

        self.text = open(document).read()
        self.text = string.lower(self.text)
        self.text = string.replace(self.text, '\n', ' ')

        self.sentence_tokenizer()

    def sentence_tokenizer(self):
        """
        Splits document into sentences
        """
        self.sentences = tokenize.sent_tokenize(self.text)

    def search_big_boy_words(self):
        for sentence in self.sentences:
            for big_boy_word in words.big_boy_words:
                if big_boy_word[0] in sentence:
                    print string.replace(sentence, big_boy_word[0], colors.FAIL + big_boy_word[0] + colors.ENDC)

if __name__ == '__main__':
    engrish = Engrish('test')
    engrish.search_big_boy_words()
