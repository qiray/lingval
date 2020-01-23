# -*- coding: utf-8 -*-

from wordcloud import WordCloud

import tokenizer
import translations

def make_wordcloud(text, filename):
    if len(text) == 0:
        print(translations.get("wordcloud_nodata"))
        return
    wordcloud = WordCloud(background_color="#FFFFFF",
        width=800, height=400, stopwords=tokenizer.get_russian_stopwords()).generate(text)
    image = wordcloud.to_image()
    image.save(filename)
