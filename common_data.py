# -*- coding: utf-8 -*-

import re
from collections import Counter

from nltk import word_tokenize, sent_tokenize

def get_common_data(text):
    # return lines, sentences, words, symbols without spaces, symbols
    return len(text.split('\n')), len(sent_tokenize(text)), len(word_tokenize(text)), len(text) - text.count(' '), len(text)

def get_top_words(words, top_count=20):
    pattern = re.compile("^[a-zA-Zа-яА-Я0-9_]+$")
    words = [x for x in words if pattern.match(x)] #remove non-words
    sorted_words_data = sorted(Counter(words).items(), key=lambda kv: kv[1], reverse=True)
    return sorted_words_data[:top_count] #list of tuples of top words
