from doctrans.constants import __root__
from doctrans.models.translator import Translator
from doctrans.models.option import Option, Lang, Extension
from collections import defaultdict
from typing import Tuple, Dict, List
from fitz import fitz
import doctrans.lang.google as google
from fitz import Document as FitzDocument, Page as FitzPage, Rect as FitzRect
import os


# Rect = Tuple[float, float, float, float]        # x0, y0, x1, y1
FontKey = Tuple[str, float, float]              # font-family, font-size, font-color


class TextBlock:
    def __init__(self, text: str, rect: FitzRect, font_key: FontKey):
        self.rect = rect
        self.text = text
        self.major_font = font_key


class PymupdfTranslator(Translator):
    def __init__(self, option: Option):
        super().__init__(option)
        self.file = None
        self.pages = None
        self.major_font = None

    def read(self, input_path: str) -> None:
        self.file = fitz.open(input_path)
        pages = defaultdict(list)

        for index, page in enumerate(self.file):
            for block_dict in page.getText("dict")["blocks"]:
                try:
                    bbox = block_dict['bbox']
                    text = str()
                    font_count_dict = defaultdict(int)

                    for line in block_dict['lines']:
                        for span in line['spans']:
                            font_family = span['font']
                            font_size = round(span['size'], 3)
                            font_color = span['color']
                            font_key = (font_family, font_size, font_color)

                            span_text = span['text']
                            font_count_dict[font_key] += len(span_text.strip())
                            text += span_text + ' '
                        text += '\n'
                    text += '\n'

                    major_font_key = max(font_count_dict, key=lambda k: font_count_dict[k])
                    pages[index].append(TextBlock(
                        rect=FitzRect(bbox[0], bbox[1], bbox[2], bbox[3]),
                        font_key=major_font_key,
                        text=text
                    ))

                except:
                    pass

        # calculate document major font
        font_key_count_dict = defaultdict(int)
        for page in pages.values():
            for text_block in page:
                font_key = text_block.major_font
                font_key_count_dict[font_key] += len(text_block.text)
        document_major_font = max(font_key_count_dict, key=lambda key: font_key_count_dict[key])

        # filter text-blocks with document major font
        filtered_pages = dict()

        for index, page in pages.items():
            filtered_pages[index] = list(filter(lambda block: block.major_font == document_major_font, page))

        self.major_font = document_major_font
        self.pages = filtered_pages

    # Simple Translation
    # def translate(self) -> None:
    #     translated_pages = defaultdict(list)
    #     for index, page in self.pages.items():
    #         for text_block in page:
    #             input_text = text_block.text.replace('-\n', '').replace('\n', '')
    #             translated_pages[index].append(TextBlock(
    #                 rect=text_block.rect,
    #                 font_key=text_block.major_font,
    #                 text=google.translate(input_text, self.option.from_lang, self.option.to_lang)
    #             ))
    #
    #     self.pages = translated_pages

    # Translation with Thread
    def translate(self) -> None:
        def translateTextBlock(text_block: TextBlock) -> TextBlock:
            input_text = text_block.text.replace('-\n', '').replace('\n', '')
            return TextBlock(
                rect=text_block.rect,
                font_key=text_block.major_font,
                text=google.translate(input_text, self.option.from_lang, self.option.to_lang)
            )

        try:
            from multiprocessing.dummy import Pool
            translated_pages = defaultdict(list)
            pool = Pool(4)

            for index, page in self.pages.items():
                page_translation_result = pool.map(translateTextBlock, page)
                translated_pages[index] = page_translation_result

            self.pages = translated_pages

            pool.close()
            pool.join()

        except Exception as e:
            raise e

    def save(self, output_path: str) -> None:
        # Write it on the virtual document, and find max-font-size
        font_family, font_size, font_color = self.major_font
        font_name = self.option.font.value
        font_filepath = os.path.join(__root__, f"fonts/{font_name}.ttf")
        max_font_size = font_size

        success = False
        while not success:
            temp_doc: FitzDocument = fitz.open()
            temp_page: FitzPage = temp_doc.newPage()

            text_box_list = list()
            for page in self.pages.values():
                text_box_list.extend(page)

            success = True
            for text_box in text_box_list:
                ret = fitz.utils.insertTextbox(page=temp_page,
                                               rect=text_box.rect,
                                               buffer=text_box.text,
                                               fontname=font_name,
                                               fontfile=font_filepath,
                                               fontsize=max_font_size)
                if ret < 0:
                    success = False
                    max_font_size *= 0.9
                    break

        # write it on the real doc
        doc: FitzDocument = self.file
        WHITE = 1

        for index, page in self.pages.items():
            doc_page: FitzPage = doc.loadPage(index)

            for text_box in page:
                # remove original
                doc_page.addRedactAnnot(text_box.rect, fill=WHITE)
                doc_page.apply_redactions()

                # insert TextBox
                fitz.utils.insertTextbox(page=doc_page,
                                         rect=text_box.rect,
                                         buffer=text_box.text,
                                         fontname=font_name,
                                         fontfile=font_filepath,
                                         fontsize=max_font_size)
        doc.save(output_path)
        print(f"Save at [ {output_path} ]")

    @classmethod
    def support(cls, option: Option) -> bool:
        if (
            option.from_lang in [Lang.AUTO, Lang.ENG]
            and option.to_lang in [Lang.KOR]
            and option.from_ext in [Extension.PDF]
            and option.to_ext in [Extension.PDF]
        ):
            return True
        else:
            return False
