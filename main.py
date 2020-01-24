# -*- coding: utf-8 -*-

import sys
from multiprocessing import Process, Lock

import argparse
import nltk

import common
import nltk_analyze
import make_wordcloud
import tokenizer
import dialogues
import sentiments
import translations

# TODO-list
# TODO:
# Examples
# Save results in csv files - output folder?
# get facts?

# https://proglib.io/p/fun-nlp
# https://en.wikipedia.org/wiki/Bag-of-words_model
# https://monkeylearn.com/text-analysis/
# https://en.wikipedia.org/wiki/Natural_language_processing

APP_NAME="Lingval"
VERSION_MAJOR = 0
VERSION_MINOR = 0
VERSION_BUILD = 1

def check_nltk_package(findname, downloadname):
    try:
        nltk.data.find(findname)
    except LookupError:
        print(translations.get("nltk_downloading"))
        nltk.download(downloadname)

def read_file(filename):
    with open(filename, 'r', encoding='utf-8') as myfile:
        return myfile.read()

def common_data(text, tokens, lock):
    headers, data = nltk_analyze.get_common_data(text)
    common.print_table(("\n%s\n" % translations.get("common_data")), headers, [data], lock)

def pos_data(text, tokens, lock):
    headers, data = nltk_analyze.get_pos_data(tokens)
    common.print_table(("\n%s\n" % translations.get("POS_analysis")), headers, data, lock)

def sentences_data(text, tokens, lock):
    headers, data, max_sent = nltk_analyze.get_sentences_data(text)
    common.accuire_lock(lock)
    common.print_table(("\n%s\n" % translations.get("sentences_analysis")), headers, [data])
    print (("\n%s\n" % translations.get("longest_sentence")), max_sent)
    common.release_lock(lock)

def collocations_data(text, tokens, lock):
    common.accuire_lock(lock)
    print(("\n%s\n" % translations.get("collocations")), nltk_analyze.get_collocations(tokens))
    common.release_lock(lock)

def topwords_data(text, tokens, lock):
    headers, data = nltk_analyze.get_top_words(tokens)
    common.print_table(("\n%s\n" % translations.get("top_words")), headers, data, lock)

def dialogues_data(text, tokens, lock):
    headers, data = dialogues.get_dialogues_info(text)
    common.print_table(("\n%s\n" % translations.get("dialogues_info")), headers, data, lock)

def wordcloud_data(text, tokens, lock):
    make_wordcloud.make_wordcloud(text, 'words.png')
    make_wordcloud.make_wordcloud(' '.join(tokens), 'lemmas.png')

def sentiment_data(text, tokens, lock):
    common.accuire_lock(lock)
    print(("\n%s\n" % translations.get("sentiments_info")))
    sentiments.analyze(nltk_analyze.get_sentences(text))
    common.release_lock(lock)

analyze_functions = [common_data, dialogues_data, pos_data, sentences_data, collocations_data, topwords_data, sentiment_data, wordcloud_data]

def worker(index, lock, text, tokens):
    analyze_functions[index](text, tokens, lock)

def get_version():
    return "%d.%d.%d" % (VERSION_MAJOR, VERSION_MINOR, VERSION_BUILD)

def get_about_info():
    return ("\n" + APP_NAME + " " + get_version() + " Copyright (C) 2019-2020 Yaroslav Zotov.\n" +
        "This program comes with ABSOLUTELY NO WARRANTY.\n" +
        "This is free software under MIT license; see the LICENSE file for copying conditions.\n")

def parse_args():
    """argparse settings"""
    parser = argparse.ArgumentParser(prog=APP_NAME, 
        description='Tool for analyzing Russian fiction texts.')
    parser.add_argument('--file', type=str, help='File for analyze')
    parser.add_argument('--lang', type=str, help='Set locale')
    parser.add_argument('--about', action='store_true', help='Show about info')
    return parser.parse_args()

def main():
    """Main function"""
    args = parse_args()
    if args.about:
        print(get_about_info())
        return
    if not args.file:
        print(translations.get("missing_filename"))
        sys.exit(1)
    if args.lang:
        translations.set_locale(args.lang)

    text = read_file(args.file)
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
