# -*- coding: utf-8 -*-

import sys
from multiprocessing import Process, Lock

import nltk

import common
import nltk_analyze
import make_wordcloud
import tokenizer

# TODO-list
# TODO:
# Examples
# Save results in csv files - output folder?
# part of speech - correct names
# dialogs (?)
# Sentiment analysis (?) - https://datascience.stackexchange.com/questions/10211/sentiment-retriving-from-text-russian
# get facts?
# Translations?

# https://proglib.io/p/fun-nlp
# https://en.wikipedia.org/wiki/Bag-of-words_model
# https://monkeylearn.com/text-analysis/
# https://en.wikipedia.org/wiki/Natural_language_processing

VERSION_MAJOR = 0
VERSION_MINOR = 0
VERSION_BUILD = 1

def check_nltk_package(findname, downloadname):
    try:
        nltk.data.find(findname)
    except LookupError:
        print("Downloading NLTK data. Please wait.")
        nltk.download(downloadname)

def read_file(filename):
    with open(filename, 'r', encoding='utf-8') as myfile:
        return myfile.read()

def parser(index, lock, text, tokens):
    if index == 0: 
        headers, data = nltk_analyze.get_common_data(text)
        common.print_table("\nCommon data:\n", headers, [data], lock)
    elif index == 1:
        headers, data = nltk_analyze.get_pos_data(tokens)
        common.print_table("\nPOS analysis\n", headers, data, lock)
    elif index == 2:
        headers, data, max_sent = nltk_analyze.get_sentences_data(text)
        lock.acquire()
        common.print_table("\nSentences analysis\n", headers, [data])
        print ("\nLongest sentence:\n", max_sent)
        lock.release()
    elif index == 3:
        lock.acquire()
        print("\nCollocations:\n", nltk_analyze.get_collocations(tokens))
        lock.release()
    elif index == 4:
        headers, data = nltk_analyze.get_top_words(tokens)
        common.print_table("\nTop words:\n", headers, data, lock)
    elif index == 5:
        make_wordcloud.make_wordcloud(text, '1.png')
        make_wordcloud.make_wordcloud(' '.join(tokens), '2.png')

def main():
    """Main function"""
    if len(sys.argv) < 2:
        print("Missing filename!")
        sys.exit(1)
    text = read_file(sys.argv[1])
    tokens = tokenizer.preprocess_text(text, True)

    procs = []
    lock = Lock()
    for i in range(5):
        proc = Process(target=parser, args=(i, lock, text, tokens))
        procs.append(proc)
        proc.start()
    for proc in procs:
        proc.join()

if __name__ == '__main__':
    check_nltk_package('corpora/stopwords', 'stopwords')
    check_nltk_package('tokenizers/punkt', 'punkt')
    check_nltk_package('taggers/averaged_perceptron_tagger_ru/averaged_perceptron_tagger_ru.pickle', 'averaged_perceptron_tagger_ru')
    main()
