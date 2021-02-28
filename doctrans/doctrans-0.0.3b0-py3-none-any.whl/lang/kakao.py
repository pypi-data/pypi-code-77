from kakaotrans import Translator
from doctrans.models.option import Lang


KakaoLangMap = {
    Lang.KOR: "kr",
    Lang.ENG: "en",
    Lang.AUTO: "en",
}


def translate(text: str, from_lang: Lang, to_lang: Lang):
    translator = Translator()
    try:
        result = translator.translate(text, src=KakaoLangMap[from_lang], tgt=KakaoLangMap[to_lang])
        return result
    except Exception as e:
        return text


# TEST
if __name__ == "__main__":
    print(translate("hello, what is your name?", Lang.AUTO, Lang.KOR))
