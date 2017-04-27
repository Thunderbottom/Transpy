from googletrans import Translator
import random
import nltk, string
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


nltk.download('punkt')
stemmer = nltk.stem.porter.PorterStemmer()
remove_punctuation_map = dict((ord(char), None) for char in string.punctuation)

def stem_tokens(tokens):
    return [stemmer.stem(item) for item in tokens]

def normalize(text):
    return stem_tokens(nltk.word_tokenize(text.lower().translate(remove_punctuation_map)))

vectorizer = TfidfVectorizer(tokenizer=normalize, stop_words='english')

def cosine_sim(text1, text2):
    tfidf = vectorizer.fit_transform([text1, text2])
    return ((tfidf * tfidf.T).A)[0,1]


def main():
    trans_langs = []
    translator   = Translator()
    trans_string = input("Enter a string which you want to translate: ")
    trans_detect = translator.detect(trans_string)
    print("The language of the entered string was detected as {}".format(LANGUAGES[trans_detect.lang]))
    try:
        trans_degree = int(input("Enter the number of times to translate: "))
    except:
        print("You entered a string and not an integer, Which wasn't expected, and now you're here reading this. Congratulations, you played yourself!")
    if trans_degree > 52:
        print("52 is the maximum number languages you can translate to.\nContinuing with 'number of times to translate : 52'")
        trans_degree = 52
    trans_langs  = random.sample(list(LANGUAGES), trans_degree)
    curr_lang    = trans_detect.lang
    curr_string  = trans_string
    for language in trans_langs:
        print("{} to {}".format(LANGUAGES[curr_lang], LANGUAGES[language]))
        translation = translator.translate(curr_string, dest = language)
        print("{} -> {}\n".format(curr_string, translation.text))
        curr_lang = language
        curr_string = translation.text
    print("{} to {}".format(LANGUAGES[curr_lang], LANGUAGES[trans_detect.lang]))
    translation = translator.translate(curr_string, dest = trans_detect.lang)
    print("{} -> {}\n".format(curr_string, translation.text))
    print("Similarity between start and end: {}".format(cosine_sim(trans_string, translation.text)))



if __name__ == '__main__':
    main()
