# -*- coding: utf-8 -*-

from wordcloud import WordCloud

import tokenizer

def make_wordcloud(text, filename):
    if len(text) == 0:
        print("Warning! No data for wordcloud")
        return
    wordcloud = WordCloud(background_color="#FFFFFF",
        width=800, height=400, stopwords=tokenizer.get_russian_stopwords()).generate(text)
    image = wordcloud.to_image()
    image.save(filename)
