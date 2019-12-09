# -*- coding: utf-8 -*-

from nltk import word_tokenize, sent_tokenize

def get_common_data(text):
    # return lines, sentences, words, symbols without spaces, symbols
    return len(text.split('\n')), len(sent_tokenize(text)), len(word_tokenize(text)), len(text) - text.count(' '), len(text)
