import pkg_resources, json
from word2lex.utils.custom_vader import SentimentIntensityAnalyzer

ROOT_PATH = pkg_resources.resource_filename('word2lex', 'data/')
AVAILABLE_MODELS = ['britain',
                    'usa',
                    'canada',
                    'politics_en',
                    'news_media',
                    'twitter']

GLOBAL_DICT = {}
for c in AVAILABLE_MODELS:
    with open(ROOT_PATH + c + '.json', 'r') as fp:
        GLOBAL_DICT[c] = json.load(fp)

class Word2Lex(object):

    def __init__(self, model='politics_en'):
        if type(model)==str:
            if model in AVAILABLE_MODELS:
                self.dictionary = GLOBAL_DICT[model]
            else:
                raise ValueError("Available dictionaries are 'canada', 'usa', 'britain', 'politics_en', 'news_media' and 'twitter'.")
        else:
            self.dictionary = GLOBAL_DICT['politics_en']
        self.analyzer = SentimentIntensityAnalyzer(self.dictionary)
              
    def sentiment(self, text):
        return self.analyzer.polarity_scores(text)['compound']              
