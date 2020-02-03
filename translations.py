# -*- coding: utf-8 -*-

data = {
    "ru": {
        "missing_filename": "Отсутствует файл!",
        "file_not_found": "Файл не найден!",
        "nltk_downloading": "Загружаю данные NLTK. Пожалуйста, подождите.",
        "dialogues": "Диалоги",
        "common_data": "Общие данные:",
        "POS_analysis": "Анализ частей речи",
        "sentences_analysis": "Анализ предложений",
        "longest_sentence": "Самое длинное предложение:",
        "collocations": "Словосочетания:",
        "top_words": "Топ слова:",
        "dialogues_info": "Информация о диалогах:",
        "sentiments_info": "Информация о настроении:",
        "sentiment": "Настроение",
        "wordcloud_nodata": "Внимание! Нет данных для облака слов",

        "paragraphs": "Параграфы",
        "sentences": "Предложения",
        "words": "Слова",
        "unique_words": "Уникальные слова",
        "symbols_without_space": "Символы без пробелов",
        "total_symbols": "Всего символов",
        "word": "Слово",
        "count": "Количество",
        "POS": "Часть речи",
        "percentage": "Процент",
        "max": "Максимум",
        "average": "Среднее",
        "median": "Медиана",
        "mode": "Мода",
        "locale_not_supported": "Язык не поддерживается",
        "supported_locales": "Поддерживаемые языки",
    },
    "en": {
        "missing_filename": "Missing filename!",
        "file_not_found": "File not found!",
        "nltk_downloading": "Downloading NLTK data. Please wait.",
        "dialogues": "Dialogues",
        "common_data": "Common data:",
        "POS_analysis": "POS analysis",
        "sentences_analysis": "Sentences analysis",
        "longest_sentence": "Longest sentence:",
        "collocations": "Collocations:",
        "top_words": "Top words:",
        "dialogues_info": "Dialogues info:",
        "sentiments_info": "Sentiments info:",
        "sentiment": "Sentiment",
        "wordcloud_nodata": "Warning! No data for wordcloud",

        "paragraphs": "Paragraphs",
        "sentences": "Sentences",
        "words": "Words",
        "unique_words": "Unique words",
        "symbols_without_space": "Symbols without spaces",
        "total_symbols": "Total symbols",
        "word": "Word",
        "count": "Count",
        "POS": "POS",
        "percentage": "Percentage",
        "max": "Max",
        "average": "Average",
        "median": "Median",
        "mode": "Mode",
        "locale_not_supported": "Locale not supported",
        "supported_locales": "Supported locales",
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
            print(self.get("locale_not_supported") + ": " + lang)
            locales = ', '.join(data.keys())
            print(self.get("supported_locales") + ": " + locales)
            lang = default_lang
        self.lang = lang
        self.data = data[lang]

    def get(self, key):
        if not key in self.data:
            return key
        return self.data[key]

translation = Translation()

def set_locale(lang):
    translation.set_locale(lang)

def get(key):
    return translation.get(key)
