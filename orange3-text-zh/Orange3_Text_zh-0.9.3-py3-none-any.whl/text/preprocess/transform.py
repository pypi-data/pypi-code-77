import re
from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import strip_accents_unicode


__all__ = ['BaseTransformer', 'HtmlTransformer', 'LowercaseTransformer',
           'StripAccentsTransformer', 'UrlRemover']


class BaseTransformer:
    name = NotImplemented

    def __call__(self, data):
        """ Transforms strings in `data`.

        Arguments:
            data (str or iterable): Items to transform

        Returns:
            str or list: Transformed items

        """
        if isinstance(data, str):
            return self.transform(data)
        return [self.transform(string) for string in data]

    @classmethod
    def transform(cls, string):
        """ Transforms `string`. """
        raise NotImplementedError("Method 'transform' isn't implemented "
                                  "in '{cls}' class".format(cls=cls.__name__))

    def __str__(self):
        return self.name


class LowercaseTransformer(BaseTransformer):
    """ 所有字母转为小写. """
    name = '转为小写'

    @classmethod
    def transform(cls, string):
        return string.lower()


class StripAccentsTransformer(BaseTransformer):
    """ naïve → naive """
    name = "去除音调符号"

    @classmethod
    def transform(cls, string):
        return strip_accents_unicode(string)


class HtmlTransformer(BaseTransformer):
    """ <a href…>Some text</a> → Some text """
    name = "去除 html 标签"

    @classmethod
    def transform(cls, string):
        return BeautifulSoup(string, 'html.parser').getText()


class UrlRemover(BaseTransformer):
    """ 去除超链接. """
    name = "去除 urls"
    urlfinder = re.compile(r"((https?):((//)|(\\\\))+([\w\d:#@%/;$()~_?\+-=\\\.&](#!)?)*)")

    @classmethod
    def transform(cls, string):
        return cls.urlfinder.sub('', string)
