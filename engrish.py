import re
from string import capitalize, replace
import sys

from nltk import tokenize
import word_bank

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

        with open(document) as fd:
            self.text = fd.read()
        self.text = replace(self.text, '\n', ' ')

        self.sentence_tokenizer()

    def sentence_tokenizer(self):
        """
        Splits document into sentences
        """
        self.sentences = tokenize.sent_tokenize(self.text)

    def highlight_red(self, sentence, word, caps=False):
        word = word if not caps else capitalize(word)
        return replace(sentence, word, colors.FAIL + word + colors.ENDC)

    def search_big_boy_words(self):
        for sentence in self.sentences:
            for words in word_bank.big_boy_words:

                # highlight big boy word if exists in sentence
                if words[0] in sentence:
                    print self.highlight_red(sentence, words[0])

                # for capitalized big boy word
                elif capitalize(words[0]) in sentence:
                    print self.highlight_red(sentence, words[0], caps=True)


if __name__ == '__main__':
    document = sys.argv[1] if len(sys.argv) > 1 else 'test'
    engrish = Engrish(document)
    engrish.search_big_boy_words()
