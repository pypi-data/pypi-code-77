import os
import re

from Orange.data.io import detect_encoding
from gensim import corpora
from nltk.corpus import stopwords

from orangecontrib.text.misc import wait_nltk_data
from pathlib import Path

__all__ = ['BaseTokenFilter', 'StopwordsFilter', 'LexiconFilter', 'RegexpFilter', 'FrequencyFilter']


class BaseTokenFilter:
    name = NotImplemented

    def __call__(self, corpus):
        if len(corpus) == 0:
            return corpus
        if isinstance(corpus[0], str):
            return self.filter(corpus)
        return [self.filter(tokens) for tokens in corpus]

    def filter(self, tokens):
        return list(filter(self.check, tokens))

    def check(self, token):
        raise NotImplementedError

    def __str__(self):
        return self.name

    def set_up(self):
        """ A method for setting filters up before every __call__. """
        pass

    def tear_down(self):
        """ A method for cleaning up after every __call__. """
        pass


class WordListMixin:
    def __init__(self, word_list=None):
        self.file_path = None
        self.word_list = word_list or []

    def from_file(self, path):
        self.file_path = path
        self.word_list = []
        if not path:
            return

        for encoding in ('utf-8',
                         None,  # sys.getdefaultencoding()
                         detect_encoding(path)):
            try:
                with open(path, encoding=encoding) as f:
                    self.word_list = set(line.strip() for line in f)
            except UnicodeDecodeError:
                continue
            return
        # No encoding worked, raise
        raise UnicodeError("Couldn't determine file encoding")


class StopwordsFilter(BaseTokenFilter, WordListMixin):
    """ 删除特定语言列表或文件中的单词(tokens). """
    name = '停用词'

    @staticmethod
    @wait_nltk_data
    def supported_languages():
        # get NLTK list of stopwords
        stopwords_listdir = []
        try:
            stopwords_listdir = [file for file in
                                 os.listdir(stopwords._get_root())
                                 if file.islower()]
        except LookupError:  # when no NLTK data is available
            pass

        all_stopwords_listdir = ['中文停用词表', '哈工大停用词表', '百度停用词表', '四川大学停用词库'] + \
                                sorted(file.capitalize() for file in stopwords_listdir)

        return all_stopwords_listdir

    @wait_nltk_data
    def __init__(self, language='English', word_list=None):
        WordListMixin.__init__(self, word_list)
        super().__init__()
        self.language = language

    @property
    def language(self):
        return self._language

    @language.setter
    def language(self, value):
        self._language = value



        if not self._language:
            self.stopwords = []
        elif self._language in ['中文停用词表', '哈工大停用词表', '百度停用词表', '四川大学停用词库']:
            stop_dict = {'中文停用词表': '1cn',
                         '哈工大停用词表': '2hit',
                         '百度停用词表': '3baidu',
                         '四川大学停用词库': '4scu'}

            dir_path = Path(__file__).resolve()
            parent_path = dir_path.parent.parent
            chinese_stop_words_path = f'{str(parent_path)}/chinese_stop_words'
            # chinese_stop_word_files = [file for file in os.listdir(chinese_stop_words_path)]

            self.stopwords = set([line.strip()
                              for line in open(f'{str(chinese_stop_words_path)}/{stop_dict[self._language]}',
                                                  'r', encoding='utf-8').readlines()])
        else:
            self.stopwords = set(
                x.strip() for x in stopwords.words(self.language.lower()))

    def __str__(self):
        config = ''
        config += 'Language: {}, '.format(self.language.capitalize()) if self.language else ''
        config += 'File: {}, '.format(self.file_path) if self.file_path else ''
        return '{} ({})'.format(self.name, config.strip(', '))

    def check(self, token):
        return token not in self.stopwords and token not in self.word_list


class LexiconFilter(BaseTokenFilter, WordListMixin):
    """ 只保留文件中的词(tokens). """
    name = '词典'

    def __init__(self, lexicon=None):
        WordListMixin.__init__(self, word_list=lexicon)

    @property
    def lexicon(self):
        return self.word_list

    @lexicon.setter
    def lexicon(self, value):
        self.word_list = set(value)

    def check(self, token):
        return not self.lexicon or token in self.lexicon

    def __str__(self):
        return '{} ({})'.format(self.name, 'File: {}'.format(self.file_path))


class RegexpFilter(BaseTokenFilter):
    """ 根据正表达式删除, 默认删除标点符号. """
    name = '正则表达式'

    def __init__(self, pattern=r'\.|,|:|!|\?'):
        self._pattern = pattern
        # Compiled Regexes are NOT deepcopy-able and hence to make Corpus deepcopy-able
        # we cannot store then (due to Corpus also storing used_preprocessor for BoW compute values).
        # To bypass the problem regex is compiled before every __call__ and discarded right after.
        self.regex = None
        self.set_up()

    @property
    def pattern(self):
        return self._pattern

    @pattern.setter
    def pattern(self, value):
        self._pattern = value
        self.set_up()

    @staticmethod
    def validate_regexp(regexp):
        try:
            re.compile(regexp)
            return True
        except re.error:
            return False

    def check(self, token):
        return not self.regex.match(token)

    def __str__(self):
        return '{} ({})'.format(self.name, self.pattern)

    def set_up(self):
        """ Compile Regex before the __call__. """
        self.regex = re.compile(self.pattern)

    def tear_down(self):
        """ Delete Regex after every __call__. """
        self.regex = None


class FrequencyFilter(LexiconFilter):
    """ 只保留此区间的单词. 小数则保留对应百分比, 整数保留对应数目 """
    name = '文档频率'

    def __init__(self, min_df=0., max_df=1., keep_n=None):
        super().__init__()
        self._corpus_len = 0
        self.keep_n = keep_n
        self._max_df = max_df
        self._min_df = min_df

    def fit_filter(self, corpus):
        self._corpus_len = len(corpus)
        tokens = getattr(corpus, 'tokens', corpus)
        dictionary = corpora.Dictionary(tokens)
        dictionary.filter_extremes(self.min_df, self.max_df, self.keep_n)
        self.lexicon = dictionary.token2id.keys()
        return self(tokens), dictionary

    @property
    def max_df(self):
        if isinstance(self._max_df, int):
            return self._max_df / self._corpus_len if self._corpus_len else 1.
        else:
            return self._max_df

    @max_df.setter
    def max_df(self, value):
        self._max_df = value

    @property
    def min_df(self):
        if isinstance(self._min_df, float):
            return int(self._corpus_len * self._min_df) or 1
        else:
            return self._min_df

    @min_df.setter
    def min_df(self, value):
        self._min_df = value

    def __str__(self):
        keep = ', keep {}'.format(self.keep_n) if self.keep_n else ''
        return "{} (range [{}, {}]{})".format(self.name, self._min_df,
                                              self._max_df, keep)

    def check(self, token):
        return token in self.lexicon
