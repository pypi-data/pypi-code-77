from enum import Enum


class DocTrans(Enum):
    PYMUPDF = "pymupdf"
    PYDOCX = "pydocx"


class TextTrans(Enum):
    GOOGLE = "google"
    KAKAO = "kakao"


class Extension(Enum):
    PDF = ".pdf"
    DOCX = ".docx"


class Lang(Enum):
    AUTO = "auto"
    KOR = "ko"
    ENG = "en"


class Font(Enum):
    KO_MALGUN_GOTHIC = "malgun_gothic"
    KO_NANUM_GOTHIC = "nanum_gothic"
    KO_APPLE_GOTHIC = "apple_sd_gothic"
    KO_HY_SHIN_MEONGJO = "hy_shinmyeongjo"
    EN_TIMES_NEW_ROMAN = "times_new_roman"


class Option:
    def __init__(self,
                 doc_trans: DocTrans,
                 text_trans: TextTrans,
                 font: Font,
                 from_ext: Extension,
                 to_ext: Extension,
                 from_lang: Lang,
                 to_lang: Lang,
                 use_thread: bool):
        self.doc_trans = doc_trans
        self.text_trans = text_trans
        self.font = font
        self.from_ext = from_ext
        self.to_ext = to_ext
        self.from_lang = from_lang
        self.to_lang = to_lang
        self.use_thread = use_thread


PDF_BASIC_OPTION = Option(
    doc_trans=DocTrans.PYMUPDF,
    text_trans=TextTrans.GOOGLE,
    font=Font.KO_MALGUN_GOTHIC,
    from_ext=Extension.PDF,
    to_ext=Extension.PDF,
    from_lang=Lang.AUTO,
    to_lang=Lang.KOR,
    use_thread=True
)


DOCX_BASIC_OPTION = Option(
    doc_trans=DocTrans.PYDOCX,
    text_trans=TextTrans.GOOGLE,
    font=Font.KO_HY_SHIN_MEONGJO,
    from_ext=Extension.DOCX,
    to_ext=Extension.DOCX,
    from_lang=Lang.AUTO,
    to_lang=Lang.KOR,
    use_thread=True
)
