# -*- coding: utf-8 -*-

# import matplotlib.pyplot as plt # TODO: find why these imports are necessary in Fedora 29. A bug?
from wordcloud import WordCloud
# from gensim import corpora, models # this too

import tokenizer

def make_wordcloud(text, filename):
    if len(text) == 0:
        print("Warning! No data for wordcloud")
        return
    wordcloud = WordCloud(background_color="#FFFFFF",
        width=800, height=400, stopwords=tokenizer.get_russian_stopwords()).generate(text)
    image = wordcloud.to_image()
    image.save(filename)
