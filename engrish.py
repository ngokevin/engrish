# Requires nltk.tokenizers.punkt
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

    def purple(self, word):
        return self.HEADER + word + self.ENDC

    def blue(self, word):
        return self.OKBLUE + word + self.ENDC

    def green(self, word):
        return self.OKGREEN + word + self.ENDC

    def yellow(self, word):
        return self.WARNING + word + self.ENDC

    def red(self, word):
        return self.FAIL + word + self.ENDC


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
        self.sentence_lengths()

    def sentence_tokenizer(self):
        """
        Splits document into sentences
        """
        self.sentences = tokenize.sent_tokenize(self.text)

    def sentence_lengths(self):
        """
        Get lengths of sentences (exclude non-word tokens)
        """
        tokenized = [tokenize.word_tokenize(sentence) for sentence in self.sentences]
        for sentence in tokenized:
            for word in enumerate(sentence):
                if not re.match('[\w\d]', word[1][0]):
                    sentence.pop(word[0])
        self.sentence_lengths = [len(sentence) for sentence in tokenized]

    def highlight_red(self, sentence, word, caps=False):
        """
        Highlights in red the occurrences of word in sentence
        caps flag indicates word or phrase is capitalized
        """
        word = word if not caps else capitalize(word)
        return replace(sentence, word, self.colors.red(word))

    def highlight_suggest_diction(self, category):
        """
        Highlights words to avoid and suggests an alternative
        word if one exists
        """
        suggestions = []
        for sentence in self.sentences:
            for words in category:

                # holds sentence and list of suggested alternatives
                suggestion = ['', []]

                # allow word bank to be list of words or
                # pairs of words (bad, suggested)
                if type(words) == list:
                    bad_word = words[0]
                    suggested_words = words[1]
                elif type(words) == str:
                    bad_word = words

                # highlight bad word if exists in sentence
                found = False
                if bad_word in sentence:
                    found = True
                    suggestion[0] = self.highlight_red(sentence, bad_word)
                elif capitalize(bad_word) in sentence:
                    found = True
                    suggestion[0] = self.highlight_red(sentence, bad_word, caps=True)
                else:
                    continue

                # suggest words if possible
                if type(words) == list and found:
                    if type(suggested_words) == list:
                        for suggested_word in suggested_words:
                            suggestion[1].append(suggested_word)
                    else:
                        suggestion[1].append(suggested_words)


                suggestions.append(suggestion)
        return suggestions

    def run(self):
        word_banks = [
            ("BIG BOY WORDS", word_bank.big_boy_words),
            ("DEAD PHRASES", word_bank.dead_phrases),
            ("BUZZ WORDS", word_bank.buzz_words),
            ("REDUNDANT PHRASES", word_bank.redundant_phrases),
            ("BUSINESS JARGON", word_bank.business_jargon),
        ]

        print(self.colors.purple("RUNNING DICTION CHECK"))
        for bank in word_banks:
            suggestions = engrish.highlight_suggest_diction(bank[1])
            for suggestion in suggestions:
                print(suggestion[0])
                print(self.colors.green("Suggestions: ") + str(suggestion[1]))
                print('')


if __name__ == '__main__':

    document = sys.argv[1] if len(sys.argv) > 1 else 'test'
    engrish = Engrish(document)
    engrish.run()
