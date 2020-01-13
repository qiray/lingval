# -*- coding: utf-8 -*-

import sys
from multiprocessing import Process, Lock

import nltk

import common
import nltk_analyze
import make_wordcloud
import tokenizer
import dialogues

# TODO-list
# TODO:
# Examples
# Save results in csv files - output folder?
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

def common_data(text, tokens, lock):
    headers, data = nltk_analyze.get_common_data(text)
    common.print_table("\nCommon data:\n", headers, [data], lock)

def pos_data(text, tokens, lock):
    headers, data = nltk_analyze.get_pos_data(tokens)
    common.print_table("\nPOS analysis\n", headers, data, lock)

def sentences_data(text, tokens, lock):
    headers, data, max_sent = nltk_analyze.get_sentences_data(text)
    if lock:
        lock.acquire()
    common.print_table("\nSentences analysis\n", headers, [data])
    print ("\nLongest sentence:\n", max_sent)
    if lock:
        lock.release()

def collocations_data(text, tokens, lock):
    if lock:
        lock.acquire()
    print("\nCollocations:\n", nltk_analyze.get_collocations(tokens))
    if lock:
        lock.release()

def topwords_data(text, tokens, lock):
    headers, data = nltk_analyze.get_top_words(tokens)
    common.print_table("\nTop words:\n", headers, data, lock)

def dialogues_data(text, tokens, lock):
    headers, data = dialogues.get_dialogues_info(text)
    common.print_table("\nDialogues info:\n", headers, data, lock)

def wordcloud_data(text, tokens, lock):
    make_wordcloud.make_wordcloud(text, 'words.png')
    make_wordcloud.make_wordcloud(' '.join(tokens), 'lemmas.png')

analyze_functions = [common_data, dialogues_data, pos_data, sentences_data, collocations_data, topwords_data, wordcloud_data]

def worker(index, lock, text, tokens):
    analyze_functions[index](text, tokens, lock)

def main():
    """Main function"""
    if len(sys.argv) < 2:
        print("Missing filename!")
        sys.exit(1)
    text = read_file(sys.argv[1])
    tokens = tokenizer.preprocess_text(text, True)

    procs = []
    lock = Lock()
    for i in range(len(analyze_functions)):
        proc = Process(target=worker, args=(i, lock, text, tokens))
        procs.append(proc)
        proc.start()
    for proc in procs:
        proc.join()

if __name__ == '__main__':
    check_nltk_package('corpora/stopwords', 'stopwords')
    check_nltk_package('tokenizers/punkt', 'punkt')
    check_nltk_package('taggers/averaged_perceptron_tagger_ru/averaged_perceptron_tagger_ru.pickle', 'averaged_perceptron_tagger_ru')
    main()
