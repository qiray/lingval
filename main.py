# -*- coding: utf-8 -*-

import sys

import nltk

import tokenizer
import make_wordcloud
import common_data

# TODO-list
# TODO:
# common data - text length, words and lines count
# nltk collocations
# wordclouds and top words
# part of speech analysis
# sentences analysis - count
# topic analysis
# dialogs (?)
# Sentiment analysis (?)
# different words count

# https://proglib.io/p/fun-nlp
# https://zen.yandex.ru/media/id/5b5ef1021a66a400a9961af1/vvedenie-v-obrabotku-jivogo-iazyka-s-pomosciu-python-36-i-nltk-chast-2-analiz-teksta-na-kliuchevye-slova-regexp-5ce2ad76b3217a00b3887fa9
# https://en.wikipedia.org/wiki/Bag-of-words_model
# http://neerc.ifmo.ru/wiki/index.php?title=%D0%9E%D0%B1%D1%80%D0%B0%D0%B1%D0%BE%D1%82%D0%BA%D0%B0_%D0%B5%D1%81%D1%82%D0%B5%D1%81%D1%82%D0%B2%D0%B5%D0%BD%D0%BD%D0%BE%D0%B3%D0%BE_%D1%8F%D0%B7%D1%8B%D0%BA%D0%B0&mobileaction=toggle_view_desktop
# https://monkeylearn.com/text-analysis/
# https://en.wikipedia.org/wiki/Natural_language_processing
# https://www.nltk.org/book/ch03.html

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
    with open(filename, 'r') as myfile:
        return myfile.read()

def main():
    """Main function"""
    text = read_file(sys.argv[1])
    # print(tokenizer.preprocess_text(text))
    # print(' '.join(tokenizer.preprocess_text(text)))
    print(common_data.get_common_data(text))
    # make_wordcloud.make_wordcloud(text, '1.png')
    # make_wordcloud.make_wordcloud(' '.join(tokenizer.preprocess_text(text)), '2.png')

if __name__ == '__main__':
    check_nltk_package('corpora/stopwords', 'stopwords')
    check_nltk_package('tokenizers/punkt', 'punkt')
    main()
