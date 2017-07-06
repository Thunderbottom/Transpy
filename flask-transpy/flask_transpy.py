import random
import string
import nltk

from googletrans import Translator
from sklearn.feature_extraction.text import TfidfVectorizer

LANGUAGES = {
    "af": "Afrikaans",
    "sq": "Albanian",
    "ar": "Arabic",
    "be": "Belarusian",
    "bg": "Bulgarian",
    "ca": "Catalan",
    "zh-CN": "Chinese_simplified",
    "zh-TW": "Chinese_traditional",
    "hr": "Croatian",
    "cs": "Czech",
    "da": "Danish",
    "nl": "Dutch",
    "en": "English",
    "eo": "Esperanto",
    "et": "Estonian",
    "tl": "Filipino",
    "fi": "Finnish",
    "fr": "French",
    "gl": "Galician",
    "de": "German",
    "el": "Greek",
    "iw": "Hebrew",
    "hi": "Hindi",
    "hu": "Hungarian",
    "is": "Icelandic",
    "id": "Indonesian",
    "ga": "Irish",
    "it": "Italian",
    "ja": "Japanese",
    "ko": "Korean",
    "la": "Latin",
    "lv": "Latvian",
    "lt": "Lithuanian",
    "mk": "Macedonian",
    "ms": "Malay",
    "mt": "Maltese",
    "no": "Norwegian",
    "fa": "Persian",
    "pl": "Polish",
    "pt": "Portuguese",
    "ro": "Romanian",
    "ru": "Russian",
    "sr": "Serbian",
    "sk": "Slovak",
    "sl": "Slovenian",
    "es": "Spanish",
    "sw": "Swahili",
    "sv": "Swedish",
    "th": "Thai",
    "tr": "Turkish",
    "uk": "Ukrainian",
    "vi": "Vietnamese",
    "cy": "Welsh",
    "yi": "Yiddish",
}

# Uncomment if you need punctuation corpora
nltk.download('punkt')
word_stemmer = nltk.stem.porter.PorterStemmer()
remove_punctuation_map = dict((ord(char), None) for char in string.punctuation)


def stem_tokens(tokens):
    return [word_stemmer.stem(item) for item in tokens]


def normalize(text):
    return stem_tokens(nltk.word_tokenize(text.lower().translate(remove_punctuation_map)))

tfidf_vectorizer = TfidfVectorizer(tokenizer=normalize, stop_words='english')


def cosine_sim(text1, text2):
    try:
        tfidf = tfidf_vectorizer.fit_transform([text1, text2])
        return ((tfidf * tfidf.T).A)[0, 1]
    except ValueError:
        print("The string cannot be translated since it only contains stopwords (no proper meaning)")
        return 0


def get_items(input_string, iterations):
    trans_langs = []
    lang_list = []
    trans_list = []
    og_trans = []
    translator = Translator()
    trans_detect = translator.detect(input_string)
    if iterations > 52:
        iterations = 52
    trans_langs = random.sample(list(LANGUAGES), iterations)
    curr_lang = trans_detect.lang
    curr_string = input_string
    lang_list.append(LANGUAGES[trans_detect.lang])
    for language in trans_langs:
        lang_list.append(LANGUAGES[language])
        translation = translator.translate(curr_string, dest=language)
        trans_list.append(translation.text)
        og_trans.append((translator.translate(curr_string, dest=trans_detect.lang)).text)
        curr_lang = language
        curr_string = translation.text
    translation = translator.translate(curr_string, dest=trans_detect.lang)
    trans_list.append(translation.text)
    lang_list.append(LANGUAGES[trans_detect.lang])
    cos_val = cosine_sim(input_string, translation.text)
    return trans_list, og_trans, lang_list, cos_val
