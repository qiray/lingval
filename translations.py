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

    def __new__(cls, lang=default_lang):
        """Singleton"""
        if not hasattr(cls, 'instance'):
            cls.instance = super(Translation, cls).__new__(cls)
        return cls.instance

    def __init__(self, lang=default_lang):
        self.set_locale(lang)

    def set_locale(self, lang):
        if not lang in data:
            lang = default_lang
        self.lang = lang
        self.data = data[lang]

    def get(self, key):
        if not key in self.data:
            return key
        return self.data[key]
