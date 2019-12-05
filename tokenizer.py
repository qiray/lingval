
# -*- coding: utf-8 -*-

import string

import pymorphy2
from nltk import word_tokenize
from nltk.corpus import stopwords
from stop_words import get_stop_words

def get_russian_stopwords():
    russian_stopwords = stopwords.words("russian") #init stopwords list
    russian_stopwords.extend(get_stop_words('ru')) #update stopwords list
    return russian_stopwords

def preprocess_text(text, remove_stopwords=False):
    '''Convert text to tokens list'''
    tokens = word_tokenize(text)
    morph = pymorphy2.MorphAnalyzer()
    tokens = [morph.parse(t)[0].normal_form for t in tokens]
    if remove_stopwords:
        tokens = [token for token in tokens if token not in get_russian_stopwords()\
            and token != " " and token.strip() not in string.punctuation]
    return tokens
