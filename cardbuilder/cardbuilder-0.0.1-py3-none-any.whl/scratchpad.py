from common import *
from common.languages import *
from common.util import enable_console_reporting
from data_sources.en_to_ja import EJDictHand, GeneDict
from data_sources.ja_to_ja import NhkPitchAccent
from data_sources.tatoeba import TatoebaExampleSentences
from word_sources.en import SvlWords

if __name__ == '__main__':
    enable_console_reporting()
    pa = NhkPitchAccent()
    d = pa.lookup_word('開く')
    b = pa.lookup_word('悪意')

    dict = EJDictHand()

    d2 = dict.lookup_word('last')
    wf = WordFrequency()
    wf2 = WordFrequency()
    s = SvlWords(wf)
    a = s[1]

    t = TatoebaExampleSentences(ENGLISH, JAPANESE)

    g = GeneDict()

    print('ddd')
    print('debug')