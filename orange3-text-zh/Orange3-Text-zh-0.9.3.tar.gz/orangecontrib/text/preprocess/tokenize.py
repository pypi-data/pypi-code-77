import re
from nltk import tokenize
import jieba
import pkuseg

from orangecontrib.text.misc import wait_nltk_data

__all__ = ['BaseTokenizer', 'WordPunctTokenizer', 'PunktSentenceTokenizer',
           'RegexpTokenizer', 'WhitespaceTokenizer', 'TweetTokenizer', 'Jieba']


class BaseTokenizer:
    """ Breaks a string into sequence of tokens. """
    tokenizer = NotImplemented
    name = 'Tokenizer'

    def __call__(self, sent):
        if isinstance(sent, str):
            return self.tokenize(sent)
        return self.tokenize_sents(sent)

    def tokenize(self, string):
        return list(filter(lambda x: x != '', self.tokenizer.tokenize(string)))

    def tokenize_sents(self, strings):
        return [self.tokenize(string) for string in strings]

    def __str__(self):
        return self.name

    def on_change(self):
        pass

    def set_up(self):
        """ A method for setting filters up before every __call__. """
        pass

    def tear_down(self):
        """ A method for cleaning up after every __call__. """
        pass


class WordPunctTokenizer(BaseTokenizer):
    """ 根据单词分词, 保留标点. This example. → (This), (example), (.)"""
    tokenizer = tokenize.WordPunctTokenizer()
    name = 'Word & Punctuation'


class PunktSentenceTokenizer(BaseTokenizer):
    """ 根据句子分词. This example. Another example. → (This example.), (Another example.) """
    tokenizer = tokenize.PunktSentenceTokenizer()
    name = 'Sentence'

    @wait_nltk_data
    def __init__(self):
        super().__init__()


class WhitespaceTokenizer(BaseTokenizer):
    """ 根据空白分词. This example. → (This), (example.)"""
    tokenizer = tokenize.WhitespaceTokenizer()
    name = 'Whitespace'


class RegexpTokenizer(BaseTokenizer):
    """ 使用正则表达式分词. """
    name = 'Regexp'

    def __init__(self, pattern=r'\w+'):
        self._pattern = pattern
        # Compiled Regexes are NOT deepcopy-able and hence to make Corpus deepcopy-able
        # we cannot store then (due to Corpus also storing used_preprocessor for BoW compute values).
        # To bypass the problem regex is compiled before every __call__ and discarded right after.
        self.tokenizer = None
        self.set_up()

    @property
    def pattern(self):
        return self._pattern

    @pattern.setter
    def pattern(self, value):
        self._pattern = value
        self.set_up()
        self.on_change()

    def __str__(self):
        return '{} ({})'.format(self.name, self.pattern)

    @staticmethod
    def validate_regexp(regexp):
        try:
            re.compile(regexp)
            return True
        except re.error:
            return False

    def set_up(self):
        self.tokenizer = tokenize.RegexpTokenizer(self.pattern)

    def tear_down(self):
        self.tokenizer = None


class TweetTokenizer(BaseTokenizer):
    """ 预训练的推特分词器.保留表情符号. This example. :-) #simple → (This), (example), (.), (:-)), (#simple) """
    tokenizer = tokenize.TweetTokenizer()
    name = 'Tweet'


class Jieba(BaseTokenizer):
    """ 结巴中文分词 """
    jieba.enable_paddle()  # 启动paddle模式
    name  = '结巴中文分词'
    tokenizer = jieba

    def __call__(self, sent):
        if isinstance(sent, str):
            return self.tokenize(sent)
        return self.tokenize_sents(sent)

    def tokenize(self, string):
        return list(filter(lambda x: x != '', self.tokenizer.cut(string, use_paddle=True)))

    def tokenize_sents(self, strings):
        return [self.tokenize(string) for string in strings]


class PKU(BaseTokenizer):
    """ 北大多领域中文分词工具 """
    name  = '北大中文分词'
    models = ['default', 'news', 'web', 'medicine', 'tourism']
    # tokenizer = pkuseg.pkuseg()

    def __init__(self, model_index=0):
        self._model_index = model_index
        self.tokenizer = pkuseg.pkuseg(model_name=self.models[self.model_index])

    @property
    def model_index(self):
        return self._model_index

    @model_index.setter
    def model_index(self, value):
        self._model_index = value
        self.tokenizer = pkuseg.pkuseg(model_name=self.models[self.model_index])

    def __call__(self, sent):
        if isinstance(sent, str):
            return self.tokenize(sent)
        return self.tokenize_sents(sent)

    def tokenize(self, string):
        return list(filter(lambda x: x != '', self.tokenizer.cut(string)))

    def tokenize_sents(self, strings):
        return [self.tokenize(string) for string in strings]
