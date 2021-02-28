from google_trans_new import google_translator
from doctrans.models.option import Lang


def translate(text: str, from_lang: Lang, to_lang: Lang):
    translator = google_translator()
    try:
        result = translator.translate(text, lang_src=from_lang.value, lang_tgt=to_lang.value)
        return result
    except Exception as e:
        return text


# TEST
if __name__ == "__main__":
    print(translate("hello, what is your name?", Lang.AUTO, Lang.KOR))
