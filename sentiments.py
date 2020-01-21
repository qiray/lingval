# -*- coding: utf-8 -*-

from dostoevsky.tokenization import RegexTokenizer
from dostoevsky.models import FastTextSocialNetworkModel

def downloader():
    """
    Based on https://github.com/bureaucratic-labs/dostoevsky/blob/master/bin/dostoevsky
    """
    import os
    from dostoevsky.data import DataDownloader, DATA_BASE_PATH, AVAILABLE_FILES
    downloader = DataDownloader()
    arguments = ["fasttext-social-network-model"]
    for filename in arguments:
        if filename not in AVAILABLE_FILES:
            raise ValueError(f'Unknown package: {filename}')
        source, destination = AVAILABLE_FILES[filename]
        destination_path: str = os.path.join(DATA_BASE_PATH, destination)
        if os.path.exists(destination_path):
            continue
        downloader.download(source=source, destination=destination)

def analyze(sentences):
    downloader()
    model = FastTextSocialNetworkModel(tokenizer=RegexTokenizer())
    results = model.predict(sentences)
    result = {}
    for sentiment in results:
        for k in sentiment:
            if k not in result:
                result[k] = 0
            result[k] += sentiment[k]
    print(result)
