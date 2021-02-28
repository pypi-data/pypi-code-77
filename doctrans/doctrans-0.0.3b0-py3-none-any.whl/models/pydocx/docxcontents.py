from docx.oxml.text.font import CT_Fonts, CT_Color, CT_HpsMeasure


def _is_translated_text(par):
    _main_text_styles = ["Normal", "BODY_TEXT", "BODY_TEXT_2", "BODY_TEXT_3", 'CAPTION', "PLAIN_TEXT"]
    return (not par.style.builtin) or par.style.name in _main_text_styles


class Tabl:
    def __init__(self, table_id):
        self.table_id = table_id


class Par:
    doc_font = None

    def __init__(self, par_id: int):
        self.par_id = par_id

    @property
    def id(self):
        return self.par_id

    @classmethod
    def majorfont_policy(cls, parfont, parfont_freq, parlength) -> bool:
        return (parfont == cls.doc_font) or ((parlength > 15) and ((parfont_freq / parlength) > 0.6))


class TextPar(Par):
    def __init__(self, par_id: int, runs: list):
        super(TextPar, self).__init__(par_id)
        self.runs = runs
        self.sentences = []
        self.font_count = dict()
        self.doc_font = None
        self._longest_run = (-1, -1, (None, None, None))

    def parse(self, tokenizer):
        text = ""
        for run_id, r in enumerate(self.runs):
            text += r.text
            font_id = self._get_fontid(r)
            length = len(r.text)
            if length > self._longest_run[1]:
                self._longest_run = (run_id, length, font_id)

            if font_id in self.font_count:
                self.font_count[font_id] += length
            else:
                self.font_count[font_id] = length
        self.sentences = tokenizer.sent_tokenize(text)

    @staticmethod
    def _get_fontid(run):
        rPr = run.element.rPr
        size = fontname = color = None
        if rPr is None:
            return size, color, fontname
        for prop in rPr:
            if isinstance(prop, CT_Fonts):
                fontname = prop.ascii if prop.ascii is not None else prop.hAnsi
            if isinstance(prop, CT_HpsMeasure):
                size = prop.val
            if isinstance(prop, CT_Color):
                color = prop
        return size, color, fontname

    @property
    def text(self):
        return ''.join(self.sentences)

    @property
    def mostfont(self) -> tuple:
        key = max(self.font_count, key=lambda k: self.font_count[k])
        return key, self.font_count[key]

    @property
    def majorfont(self):
        """
        get most frequent font
        if that font's frequenty is less than 0.6 return None
        """
        most_font, most_freq = self.mostfont
        text_length = sum([l for k, l in self.font_count.items()])
        if Par.majorfont_policy(most_font, most_freq, text_length):
            return most_font
        else:
            return None

    @property
    def majorrunid(self):
        majorfont = self.majorfont
        if majorfont is not None:
            if majorfont == self._longest_run[2]:
                return self._longest_run[0]
            for run_id, r in enumerate(self.runs):
                font_id = self._get_fontid(r)
                if font_id == majorfont:
                    return run_id
        return self._longest_run[0]

    @property
    def firstsentence(self):
        if self.sentences:
            return self.sentences[0]
        return None

    @firstsentence.setter
    def firstsentence(self, val):
        if val == "":
            self.sentences.pop(0)
        else:
            self.sentences[0] = val

    @property
    def lastsentence(self):
        if self.sentences:
            return self.sentences[-1]
        return None

    @lastsentence.setter
    def lastsentence(self, val):
        if val == "":
            self.sentences.pop()
        else:
            self.sentences[-1] = val


class MediaPar(Par):
    def __init__(self, par_id):
        super(MediaPar, self).__init__(par_id)


class NoneTranslatedText(Par):
    def __init__(self, par_id):
        super(NoneTranslatedText, self).__init__(par_id)


class SubTextPar(TextPar):
    def __init__(self, par_id, run_range, runs):
        super(SubTextPar, self).__init__(par_id, runs)
        self.run_range = run_range


class SubMediaPar(MediaPar):
    def __init__(self, par_id, run_range):
        super(SubMediaPar, self).__init__(par_id)
        self.runrange = run_range


class SubParFactory:
    @classmethod
    def make_text_subpar(cls, par_id, run_range, runs):
        return SubTextPar(par_id, run_range, runs)

    @classmethod
    def make_media_subpar(cls, par_id, run_range):
        return SubMediaPar(par_id, run_range)


class MultiMediaPar:
    def __init__(self, par_id, runs):
        self.runs = runs
        self.par_id = par_id
        self.doc_font = None
        self.subpars = []

    def parse(self, tokenizer):
        runtypes = []
        for run_id, r in enumerate(self.runs):
            if self._istext(r):
                runtypes.append("t")
            else:
                runtypes.append("m")
        range_ = [0]
        for i in range(1, len(runtypes)+1):
            range_.append(i)
            if i < len(runtypes) and runtypes[i] == runtypes[i - 1]:
                pass
            else:
                lower, upper = (range_[0], range_[-1])
                subpar = self._makesubpar(runtypes[lower], (lower, upper), tokenizer)
                self.subpars.append(subpar)
                range_ = [range_[-1]]

    @staticmethod
    def _istext(run) -> bool:
        run_xml = run._r.xml
        return "<w:t" in run_xml and len(run.text) > 0

    def _makesubpar(self, _type, _range, tokenizer):
        lower, upper = _range
        par_id = self.par_id
        runs = self.runs[lower:upper]
        if _type == "t":
            subtext = SubParFactory.make_text_subpar(par_id, _range, runs)
            subtext.parse(tokenizer)
            return subtext
        else:
            return SubParFactory.make_media_subpar(par_id, _range)

    @property
    def text(self):
        text = ""
        for subpar in self.subpars:
            if isinstance(subpar, SubTextPar):
                text += subpar.text
            else:
                text += self.tokenstring
        return text

    @property
    def tokenstring(self):
        token = "\"JBDB\""
        return f"{token}"

    @property
    def mostfont(self) -> (object, int):
        font_count = dict()
        for subpar in self.subpars:
            if isinstance(subpar, SubTextPar):
                subfont_count = subpar.font_count
                for key, item in subfont_count.items():
                    if key in font_count:
                        font_count[key] += item
                    else:
                        font_count[key] = item
        most_font = max(font_count, key=lambda k: font_count[k])
        most_freq = font_count[most_font]
        return most_font, most_freq

    @property
    def majorfont(self):
        most_font, most_freq = self.mostfont
        text_length = sum([len(sup.text) for sup in self.subpars if isinstance(sup, SubTextPar)])
        try:
            if Par.majorfont_policy(most_font, most_freq, text_length):
                return most_font
            else:
                return None
        except ZeroDivisionError:
            print(f"font freq division zero error : par{self.par_id}")
            print(self.text)
            return None

    @property
    def firstsentence(self):
        if isinstance(self.subpars[0], SubTextPar):
            return self.subpars[0].firstsentence
        return None

    @firstsentence.setter
    def firstsentence(self, val):
        if isinstance(self.subpars[0], SubTextPar):
            self.subpars[0].firstsentence = val

    @property
    def lastsentence(self):
        if isinstance(self.subpars[-1], SubTextPar):
            return self.subpars[-1].firstsentence
        return None

    @lastsentence.setter
    def lastsentence(self, val):
        if isinstance(self.subpars[-1], SubTextPar):
            self.subpars[-1].firstsentence = val

    @property
    def num_of_subpars(self):
        return len(self.subpars)

    @property
    def num_of_textpars(self):
        num = 0
        for p in self.subpars:
            if isinstance(p, SubTextPar):
                num += 1
        return num

    @property
    def num_of_mediapars(self):
        num = 0
        for p in self.subpars:
            if isinstance(p, SubMediaPar):
                num += 1
        return num


class ParFactory:
    @classmethod
    def make_par_content(cls, par_id, par, tokenizer):
        partype = cls.partype(par)
        runs = par.runs
        if partype == "Text":
            textpar = TextPar(par_id, runs)
            textpar.parse(tokenizer)
            return textpar
        if partype == "Media":
            return MediaPar(par_id)
        if partype == "Multi":
            multipar = MultiMediaPar(par_id, runs)
            multipar.parse(tokenizer)
            return multipar
        if partype == "None":
            return NoneTranslatedText(par_id)
        return None

    @classmethod
    def partype(cls, par):
        txtrcnt = mediarcnt = 0
        for r in par.runs:
            if "<w:t" in r._r.xml:
                if len(r.text) > 0:
                    txtrcnt += 1
            else:
                mediarcnt += 1
        hastext = txtrcnt > 0
        hasmedia = mediarcnt > 0
        if hastext and (not hasmedia):
            if _is_translated_text(par):
                return "Text"
            else:
                return "None"
        if hastext and hasmedia:
            if _is_translated_text(par):
                return "Multi"
        if (not hastext) and hasmedia:
            return "Media"
        return None
