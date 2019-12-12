# -*- coding: utf-8 -*-

import re
from collections import Counter
from operator import itemgetter

import tabulate
from nltk import word_tokenize, sent_tokenize, collocations, pos_tag

def get_common_data(text):
    # return lines, sentences, words, symbols without spaces, symbols
    headers = ["Lines", "Sentences", "Words", "Symbols without spaces", "Total symbols"]
    return headers, [len(text.split('\n')), len(sent_tokenize(text)), len(word_tokenize(text)), len(text) - text.count(' '), len(text)]

def get_top_words(words, top_count=20):
    pattern = re.compile("^[a-zA-Zа-яА-Я0-9_]+$")
    words = [x for x in words if pattern.match(x)] #remove non-words
    sorted_words_data = sorted(Counter(words).items(), key=lambda kv: kv[1], reverse=True)
    headers = ["Word", "Count"]
    return headers, sorted_words_data[:top_count] #list of tuples of top words

def get_collocations(tokens, count=10):
    bigram_measures = collocations.BigramAssocMeasures()
    # Best results with window_size, freq_filter of: (2,1) (2,2) (5,1)
    finder = collocations.BigramCollocationFinder.from_words(tokens, window_size=2)
    finder.apply_freq_filter(1)
    colls = finder.nbest(bigram_measures.likelihood_ratio, count)
    return colls

def get_pos_data(tokens):
    data = pos_tag(tokens, lang='rus')
    counts = Counter(tag for word, tag in data)
    total = sum(counts.values())
    # print(dict((word, float(count)/total) for word,count in counts.items()))
    result = dict((word, count) for word,count in counts.items())
    sorted_counts = sorted(result.items(), key=itemgetter(1), reverse=True)
    headers = ["POS", "Count", "Percentage"]
    return headers, sorted_counts

def print_table(title, headers, data):
    if title:
        print(title)
    print(tabulate.tabulate(data, headers=headers, numalign="right"))
