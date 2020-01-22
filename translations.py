# -*- coding: utf-8 -*-

data = {
    "ru": {
        "missing_filename": "Отсутствует файл!",
    },
    "en": {
        "missing_filename": "Missing filename!",
    }
}
default_lang = "en"

class Translation():
    def __init__(self, lang=default_lang):
        if not lang in data:
            lang = default_lang
        self.lang = lang
        self.data = data[lang]
    def get(self, key):
        if not key in self.data:
            return key
        return self.data[key]
