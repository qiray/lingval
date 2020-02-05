# -*- coding: utf-8 -*-

import re
import statistics
from collections import Counter
from operator import itemgetter

import tabulate
from nltk import word_tokenize, sent_tokenize, collocations, pos_tag

import translations

def get_common_data(text):
    ''' return paragraphs, sentences, words, symbols without spaces, symbols '''
    headers = [
        translations.get("paragraphs"),
        translations.get("sentences"),
        translations.get("words"),
        translations.get("unique_words"),
        translations.get("symbols_without_space"),
        translations.get("total_symbols")
    ]
    words = word_tokenize(text, language="russian")
    lines = text.split('\n')
    lines_count = len([x for x in lines if x and not x.isspace()])
    return headers, [lines_count, len(sent_tokenize(text, language="russian")), len(words), len(set(words)), len(text) - text.count(' '), len(text)]

def get_top_words(words, top_count=20):
    sorted_words_data = sorted(Counter(words).items(), key=lambda kv: kv[1], reverse=True)
    headers = [
        translations.get("word"),
        translations.get("count")
    ]
    return headers, sorted_words_data[:top_count] #list of tuples of top words

def get_collocations(tokens, count=10):
    bigram_measures = collocations.BigramAssocMeasures()
    # Best results with window_size, freq_filter of: (2,1) (2,2) (5,1)
    finder = collocations.BigramCollocationFinder.from_words(tokens, window_size=2)
    finder.apply_freq_filter(1)
    colls = finder.nbest(bigram_measures.likelihood_ratio, count)
    return colls

pos_names = {
    "S" : "существительное",
    "A" : "прилагательное",
    "NUM" : "числительное",
    "ANUM" : "числительное-прилагательное",
    "V" : "глагол",
    "ADV" : "наречие",
    "PRAEDIC" : "предикатив",
    "PARENTH" : "вводное слово",
    "SPRO" : "местоимение-существительное",
    "APRO" : "местоимение-прилагательное",
    "ADVPRO" : "местоимение-наречие",
    "PRAEDICPRO" : "местоимение-предикатив",
    "PR" : "предлог",
    "CONJ" : "союз",
    "PART" : "частица",
    "INTJ" : "междометие",
}

def get_pos_name(pos):
    pos = re.sub('[-=].*$', '', pos)
    if pos in pos_names:
        return pos_names[pos]
    return pos

def get_pos_data(tokens):
    result = pos_tag(tokens, lang='rus')
    counts = Counter(get_pos_name(tag) for word, tag in result)
    total = sum(counts.values())
    result = list((word, count, float(count)/total*100) for word,count in counts.items())
    sorted_counts = sorted(result, key=itemgetter(1), reverse=True)
    headers = [
        translations.get("POS"),
        translations.get("count"),
        translations.get("percentage")
    ]
    return headers, sorted_counts

def get_sentences(text):
    return sent_tokenize(text, language="russian")

def get_sentences_data(text):
    sentences = get_sentences(text)
    pattern = re.compile("[a-zA-Zа-яА-Я0-9_]+")
    words = [len(pattern.findall(x)) for x in sentences]
    headers = [
        translations.get("sentences"),
        translations.get("max"),
        translations.get("average"),
        translations.get("median"),
        translations.get("mode"),
    ]
    max_words = max(words)
    max_sent = sentences[words.index(max_words)]
    try:
        mode = statistics.mode(words)
    except:
        c = Counter(words)
        mode = c.most_common(1)[0][0]
    return headers, [len(sentences), max_words, statistics.mean(words), statistics.median(words), mode], max_sent
