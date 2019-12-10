
# -*- coding: utf-8 -*-

import string

import pymorphy2
from nltk.corpus import stopwords
from stop_words import get_stop_words
from pymystem3 import Mystem

def get_russian_stopwords():
    russian_stopwords = stopwords.words("russian") #init stopwords list
    russian_stopwords.extend(get_stop_words('ru')) #update stopwords list
    return russian_stopwords

def preprocess_text(text, remove_stopwords=False):
    '''Convert text to tokens list'''
    mystem = Mystem() #Create lemmatizer
    tokens = mystem.lemmatize(text.lower())
    if remove_stopwords:
        stopwords = get_russian_stopwords()
        tokens = [token for token in tokens if token not in stopwords\
            and token != " " and token.strip() not in string.punctuation]
    return tokens
