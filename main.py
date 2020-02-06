# -*- coding: utf-8 -*-

import sys
import operator
from multiprocessing import Process, Lock

import argparse
import nltk

import common
import fileio
import nltk_analyze
import make_wordcloud
import tokenizer
import dialogues
import sentiments
import translations

# TODO-list
# TODO:
# Examples
# Topics. Maybe LDA (?)

APP_NAME="lingval"
VERSION_MAJOR = 1
VERSION_MINOR = 0
VERSION_BUILD = 0

def check_nltk_package(findname, downloadname):
    try:
        nltk.data.find(findname)
    except LookupError:
        print(translations.get("nltk_downloading"))
        nltk.download(downloadname)

def read_file(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as myfile:
            return myfile.read()
    except IOError:
        print(translations.get("file_not_found"))
        sys.exit(2)
    except UnicodeDecodeError:
        print(translations.get("bad_encoding"))
        sys.exit(3)

def common_data(dirname, text, tokens, lock):
    headers, data = nltk_analyze.get_common_data(text)
    fileio.write_csv(dirname, "common_data", headers, [data])
    common.print_table(("\n%s\n" % translations.get("common_data")), headers, [data], lock)

def pos_data(dirname, text, tokens, lock):
    headers, data = nltk_analyze.get_pos_data(tokens)
    fileio.write_csv(dirname, "pos_data", headers, data)
    common.print_table(("\n%s\n" % translations.get("POS_analysis")), headers, data, lock)

def sentences_data(dirname, text, tokens, lock):
    headers, data, max_sent = nltk_analyze.get_sentences_data(text)
    fileio.write_csv(dirname, "sentences_data", headers, [data])
    fileio.write_file(dirname, "longest_sentence", max_sent)
    common.accuire_lock(lock)
    common.print_table(("\n%s\n" % translations.get("sentences_analysis")), headers, [data])
    print (("\n%s\n" % translations.get("longest_sentence")), max_sent)
    common.release_lock(lock)

def collocations_data(dirname, text, tokens, lock):
    data = nltk_analyze.get_collocations(tokens)
    fileio.write_csv(dirname, "collocations", [translations.get("word") + " 1", translations.get("word") + " 2"], data)
    common.accuire_lock(lock)
    print(("\n%s\n" % translations.get("collocations")), data)
    common.release_lock(lock)

def topwords_data(dirname, text, tokens, lock):
    headers, data = nltk_analyze.get_top_words(tokens)
    fileio.write_csv(dirname, "topwords_data", headers, data)
    common.print_table(("\n%s\n" % translations.get("top_words")), headers, data, lock)

def dialogues_data(dirname, text, tokens, lock):
    headers, data = dialogues.get_dialogues_info(text)
    fileio.write_csv(dirname, "dialogues_info", headers, data)
    common.print_table(("\n%s\n" % translations.get("dialogues_info")), headers, data, lock)

def wordcloud_data(dirname, text, tokens, lock):
    make_wordcloud.make_wordcloud(text, dirname + 'words.png')
    make_wordcloud.make_wordcloud(' '.join(tokens), dirname + 'lemmas.png')

def sentiment_data(dirname, text, tokens, lock):
    data = sentiments.analyze(nltk_analyze.get_sentences(text))
    data = dict(sorted(data.items(), key=operator.itemgetter(1), reverse=True))
    fileio.write_csv(dirname, "sentiments", [translations.get("sentiment"), translations.get("percentage")], [[k, data[k]] for k in data])
    common.accuire_lock(lock)
    print(("\n%s" % translations.get("sentiments_info")))
    print(data)
    common.release_lock(lock)

analyze_functions = [common_data, dialogues_data, pos_data, sentences_data, collocations_data, topwords_data, sentiment_data, wordcloud_data]

def worker(index, dirname, lock, text, tokens):
    analyze_functions[index](dirname, text, tokens, lock)

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
    basename = fileio.get_basename(args.file)
    dirname = fileio.get_output_path(basename)
    fileio.prepare_output(basename)

    procs = []
    lock = Lock()
    for i in range(len(analyze_functions)):
        proc = Process(target=worker, args=(i, dirname, lock, text, tokens))
        procs.append(proc)
        proc.start()
    for proc in procs:
        proc.join()

if __name__ == '__main__':
    check_nltk_package('corpora/stopwords', 'stopwords')
    check_nltk_package('tokenizers/punkt', 'punkt')
    check_nltk_package('taggers/averaged_perceptron_tagger_ru/averaged_perceptron_tagger_ru.pickle', 'averaged_perceptron_tagger_ru')
    main()
