import docx
import os
from doctrans.models.translator import Translator
from doctrans.models.option import Option, Extension
from doctrans.models.pydocx.docxcontents import Tabl, ParFactory, Par, TextPar, MultiMediaPar, SubTextPar, SubMediaPar
from doctrans.models.pydocx.tokenizer import Tokenizer
from doctrans.lang.google import translate
from doctrans.format_converter import pdf2docx, docx2pdf
from doctrans.models.pydocx.parsers import iter_block_items
from docx.table import Table
from docx.text.paragraph import Paragraph


class DocxTranslator(Translator):
    def __init__(self, option: Option):
        super().__init__(option)
        self.doc = None
        self.pars = []
        self.tokenizer = None
        self.majorfont = None

    def read(self, input_path: str) -> None:
        input_path = self._read_convert(input_path)
        self.doc = docx.Document(input_path)
        self.tokenizer = Tokenizer(text="".join([p.text for p in self.doc.paragraphs]))
        self._parse()

    def _read_convert(self, input_path):
        input_path = os.path.abspath(input_path)
        dir_path, filename = os.path.split(input_path)
        filename, extension = os.path.splitext(filename)

        if extension == Extension.PDF.value:
            docx_path = os.path.abspath(os.path.join(dir_path, filename + Extension.DOCX.value))
            pdf2docx(input_path, docx_path)
            return docx_path
        elif extension == Extension.DOCX.value:
            return input_path

    def _parse(self):
        fonts = dict()
        docx_contents = iter_block_items(self.doc)
        for par_id, content in enumerate(docx_contents):
            if isinstance(content, Paragraph):
                par = ParFactory.make_par_content(par_id, content, self.tokenizer)
                self.pars.append(par)
                if self._hastext(par):
                    font, length = par.mostfont
                    if font in fonts:
                        fonts[font] += length
                    else:
                        fonts[font] = length
            elif isinstance(content, Table):
                table = Tabl(par_id)
                self.pars.append(table)

        self.majorfont = max(fonts, key=lambda k: fonts[k])
        Par.doc_font = self.majorfont

        i = 0
        while i < len(self.pars):
            currentpar = self.pars[i]
            if self._hastext(currentpar):
                nextpar = self._nextpar(currentpar)
                if currentpar.majorfont is not None and self._hastext(nextpar):
                    self._adjust_sentences(currentpar, nextpar)
                    i = nextpar.par_id
                    continue
            i += 1

    def _nextpar(self, par):
        idx = par.par_id
        for i in range(idx + 1, min(len(self.pars), idx + 3)):
            nextpar = self.pars[i]
            if self._hastext(nextpar) and par.majorfont == nextpar.majorfont:
                return nextpar
        return None

    @staticmethod
    def _hastext(par):
        return isinstance(par, TextPar) or isinstance(par, MultiMediaPar)

    def _adjust_sentences(self, par1, par2):
        try:
            if (par1.lastsentence is None) or (par2.firstsentence is None):
                return
            inter_sent = self._merge_sentence(par1.lastsentence, par2.firstsentence)
            if inter_sent is not None:
                par1.lastsentence = inter_sent
                par2.firstsentence = ""

                # if len(par1.lastsentence) < len(par2.firstsentence):
                #     par1.lastsentence = ""
                #     par2.firstsentence = inter_sent
                # else:
                #     par1.lastsentence = inter_sent
                #     par2.firstsentence = ""

        except Exception as e:
            print(e)
            print(par1.lastsentence)
            print(">>>>>>>>>>>>>>")
            print(par2.firstsentence)

    def _merge_sentence(self, sent1, sent2):
        sents = sent1 + " " + sent2
        sents = self.tokenizer.sent_tokenize(sents)

        if len(sents) == 1:
            return sents[0]
        return None

    def translate(self, threading=True) -> None:
        if threading:
            par_ids, translated_texts = self._translate_threading()
        else:
            par_ids, translated_texts = self._translate_nothreading()
        self._write(translated_texts, par_ids)

    def _translate_threading(self):
        from multiprocessing.dummy import Pool as ThreadPool
        pool = ThreadPool(8)
        par_ids = []
        pars = []
        for par_id, p in enumerate(self.pars):
            if isinstance(p, TextPar) or isinstance(p, MultiMediaPar):
                par_ids.append(par_id)
                pars.append(p)
        try:
            translated_texts = pool.map(self._translate_request, pars)
        except Exception as e:
            raise e
        pool.close()
        pool.join()
        return par_ids, translated_texts

    def _translate_nothreading(self):
        par_ids = []
        translated_texts = []
        for par_id, p in enumerate(self.pars):
            if isinstance(p, TextPar) or isinstance(p, MultiMediaPar):
                translated_text = self._translate_request(p)
                par_ids.append(par_id)
                translated_texts.append(translated_text)
        return par_ids, translated_texts

    def _translate_request(self, p: TextPar or MultiMediaPar):
        txt = p.text
        translated_txt = txt
        if p.majorfont is not None:
            translated_txt = translate(txt, self.option.from_lang, self.option.to_lang)
        return translated_txt

    def _write(self, translated_texts: list, par_ids: list):
        for translated_text, par_id in zip(translated_texts, par_ids):
            par = self.pars[par_id]
            if isinstance(par, TextPar):
                self._write_textpar(par, translated_text)
            elif isinstance(par, MultiMediaPar):
                self._write_multimediapar(par, translated_text)

    @staticmethod
    def _write_textpar(par: TextPar, translated_text):
        for i, run in enumerate(par.runs):
            if i == par.majorrunid:
                run.text = translated_text
            else:
                run.text = ""

    def _write_multimediapar(self, par: MultiMediaPar, translated_text):
        txts = translated_text.split(par.tokenstring)
        if isinstance(par.subpars[-1], SubMediaPar) and txts[-1].rstrip() == '':
            txts.pop()
        if isinstance(par.subpars[0], SubMediaPar) and txts[0].lstrip() == '':
            txts.pop(0)

        if len(txts) != par.num_of_textpars:
            handle = self._writehandler(par)
            if not handle:
                print(f"Can't translate MultiMedia Par{par.par_id} : f{len(txts)}, f{par.num_of_textpars}.")
                print(f"Translated : {txts}")
            return

        for subpar in par.subpars:
            if isinstance(subpar, SubTextPar):
                txt = txts.pop(0)
                self._write_textpar(subpar, txt)

    def _writehandler(self, par):
        sentences = self.tokenizer.sent_tokenize(par.text)
        _subtexts = []
        subtext = ""
        subtexts = []
        subparmap = ""

        for subp in par.subpars:
            if isinstance(subp, SubTextPar):
                subparmap += "1"
            else:
                subparmap += "0"

        for sentence in sentences:
            if par.tokenstring in sentence:
                if subtext != "":
                    _subtexts.append(subtext)
                    subtext = ""
                _subtexts.append(None)
            else:
                subtext += sentence
        if subtext != "":
            _subtexts.append(subtext)

        subtextmap = ""
        for sb in _subtexts:
            if isinstance(sb, str):
                subtextmap += "1"
            else:
                subtextmap += "0"

        if len(subtextmap) < len(subparmap):
            if subparmap[0:len(subtextmap)] == subtextmap:
                for i in range(len(subtextmap), len(subparmap)):
                    if subparmap[i] == "1":
                        _subtexts.append("")
                    else:
                        _subtexts.append(None)
            if subparmap[len(subparmap)-len(subtextmap):len(subparmap)] == subtextmap:
                tmp = []
                for i in range(0, len(subtextmap)):
                    if subparmap[i] == "1":
                        tmp.append("")
                    else:
                        tmp.append(None)
                _subtexts = tmp + _subtexts
        else:
            return False

        for txt, subpar in zip(subtexts, par.subpars):
            if isinstance(subpar, SubTextPar):
                translated_txt = txt
                if txt != "":
                    translated_txt = translate(txt, self.option.from_lang, self.option.to_lang)
                self._write_textpar(subpar, translated_txt)
        return True

    def _setfont(self):
        fonts = {
            "malgun_gothic": "맑은 고딕",
            "nanum_gothic": "나눔 고딕",
            "apple_sd_gothic": "",
            "hy_shinmyeongjo": "HY신명조",
            "times_new_roman": "Times New Roman",
        }
        from docx.oxml.ns import qn
        _main_text_styles = ["Normal", "BODY_TEXT", "BODY_TEXT_2", "BODY_TEXT_3", 'CAPTION', "PLAIN_TEXT"]
        font = fonts[self.option.font.value]
        for style_name in _main_text_styles:
            if style_name in self.doc.styles:
                style = self.doc.styles[style_name]
                style._element.rPr.rFonts.set(qn('w:eastAsia'), font)

    def save(self, output_path: str) -> None:
        output_path = os.path.abspath(output_path)
        dir_path, filename = os.path.split(output_path)
        filename, extension = os.path.splitext(filename)
        self._setfont()
        if extension == Extension.DOCX.value:
            self.doc.save(output_path)
        elif extension == Extension.PDF.value:
            doc_path = os.path.join(dir_path, filename + Extension.DOCX.value)
            self.doc.save(doc_path)
            docx2pdf(doc_path, output_path)

    @classmethod
    def support(cls, option: Option) -> bool:
        if option.from_ext in [Extension.PDF, Extension.DOCX] and option.to_ext in [Extension.PDF, Extension.DOCX]:
            return True
        return False
