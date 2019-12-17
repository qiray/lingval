# -*- coding: utf-8 -*-

import re
import statistics
from collections import Counter
from operator import itemgetter

import tabulate
from nltk import word_tokenize, sent_tokenize, collocations, pos_tag

def get_common_data(text):
    # return lines, sentences, words, symbols without spaces, symbols
    headers = ["Lines", "Sentences", "Words", "Unique words", "Symbols without spaces", "Total symbols"]
    words = word_tokenize(text, language="russian")
    return headers, [len(text.split('\n')), len(sent_tokenize(text, language="russian")), len(words), len(set(words)), len(text) - text.count(' '), len(text)]

def get_top_words(words, top_count=20):
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
    result = list((word, count, float(count)/total) for word,count in counts.items())
    sorted_counts = sorted(result, key=itemgetter(1), reverse=True)
    headers = ["POS", "Count", "Percentage"]
    return headers, sorted_counts

def get_sentences_data(text):
    sentences = sent_tokenize(text, language="russian")
    words = [len(word_tokenize(x, language="russian")) for x in sentences]
    headers = ["Sentences", "Max", "Average", "Median", "Mode"]
    max_words = max(words)
    max_sent = sentences[words.index(max_words)]
    try:
        mode = statistics.mode(words)
    except:
        c = Counter(words)
        mode = c.most_common(1)[0][0]
    return headers, [len(sentences), max_words, statistics.mean(words), statistics.median(words), mode], max_sent
