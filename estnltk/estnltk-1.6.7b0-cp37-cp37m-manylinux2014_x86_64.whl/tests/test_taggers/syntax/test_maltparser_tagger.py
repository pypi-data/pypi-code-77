from collections import OrderedDict
import pkgutil

import pytest

from estnltk import Text
from estnltk.converters import dict_to_layer, layer_to_dict
from estnltk.taggers import ConllMorphTagger
from estnltk.taggers.syntax.maltparser_tagger import MaltParserTagger

from estnltk.taggers.syntax.vislcg3_syntax import check_if_vislcg_is_in_path

def check_if_conllu_is_available():
    # Check if conllu is available
    return pkgutil.find_loader("conllu") is not None

def simplify_syntax_layer( layer ):
    simpler = []
    for span in layer:
        ann = span.annotations[0]
        simpler.append( (ann.text, ann['upostag'], ann['deprel'], ann['id'], ann['head']) )
    return simpler

@pytest.mark.skipif(not check_if_conllu_is_available(),
                    reason="package conllu is required for this test")
@pytest.mark.skipif(not check_if_vislcg_is_in_path('vislcg3'),
                    reason="a directory containing vislcg3 executable must be inside the system PATH")
def test_maltparser_tagger_1():
    # Use ConllMorphTagger to prepare text for MaltParser
    conll_morph_tagger = ConllMorphTagger()
    # Case 1
    text = Text('Ilus suur karvane kass nurrus punasel diivanil. Ta on ise tee esimesel poolel. Valge jänes jooksis metsa!').tag_layer(['morph_extended'])
    conll_morph_tagger.tag(text)
    assert 'conll_morph' in text.layers
    expected_layer_dict = \
        {'ambiguous': False,
         'attributes': ('id',
                        'lemma',
                        'upostag',
                        'xpostag',
                        'feats',
                        'head',
                        'deprel',
                        'deps',
                        'misc',
                        'parent_span',
                        'children'),
         'enveloping': None,
         'meta': {},
         'name': 'maltparser_syntax',
         'parent': None,
         'serialisation_module': 'syntax_v0',
         'spans': [{'annotations': [{'deprel': '@AN>',
                                     'deps': None,
                                     'feats': OrderedDict([('sg', ''), ('nom', '')]),
                                     'head': 4,
                                     'id': 1,
                                     'lemma': 'ilus',
                                     'misc': None,
                                     'upostag': 'A',
                                     'xpostag': 'A'}],
                    'base_span': (0, 4)},
                   {'annotations': [{'deprel': '@AN>',
                                     'deps': None,
                                     'feats': OrderedDict([('sg', ''), ('nom', '')]),
                                     'head': 4,
                                     'id': 2,
                                     'lemma': 'suur',
                                     'misc': None,
                                     'upostag': 'A',
                                     'xpostag': 'A'}],
                    'base_span': (5, 9)},
                   {'annotations': [{'deprel': '@AN>',
                                     'deps': None,
                                     'feats': OrderedDict([('sg', ''), ('nom', '')]),
                                     'head': 4,
                                     'id': 3,
                                     'lemma': 'karvane',
                                     'misc': None,
                                     'upostag': 'A',
                                     'xpostag': 'A'}],
                    'base_span': (10, 17)},
                   {'annotations': [{'deprel': '@SUBJ',
                                     'deps': None,
                                     'feats': OrderedDict([('sg', ''), ('nom', '')]),
                                     'head': 5,
                                     'id': 4,
                                     'lemma': 'kass',
                                     'misc': None,
                                     'upostag': 'S',
                                     'xpostag': 'S'}],
                    'base_span': (18, 22)},
                   {'annotations': [{'deprel': 'ROOT',
                                     'deps': None,
                                     'feats': OrderedDict([('indic', ''),
                                                           ('impf', ''),
                                                           ('ps3', ''),
                                                           ('sg', '')]),
                                     'head': 0,
                                     'id': 5,
                                     'lemma': 'nurru',
                                     'misc': None,
                                     'upostag': 'V',
                                     'xpostag': 'V'}],
                    'base_span': (23, 29)},
                   {'annotations': [{'deprel': '@AN>',
                                     'deps': None,
                                     'feats': OrderedDict([('sg', ''), ('ad', '')]),
                                     'head': 7,
                                     'id': 6,
                                     'lemma': 'punane',
                                     'misc': None,
                                     'upostag': 'A',
                                     'xpostag': 'A'}],
                    'base_span': (30, 37)},
                   {'annotations': [{'deprel': '@ADVL',
                                     'deps': None,
                                     'feats': OrderedDict([('sg', ''), ('ad', '')]),
                                     'head': 5,
                                     'id': 7,
                                     'lemma': 'diivan',
                                     'misc': None,
                                     'upostag': 'S',
                                     'xpostag': 'S'}],
                    'base_span': (38, 46)},
                   {'annotations': [{'deprel': '@Punc',
                                     'deps': None,
                                     'feats': OrderedDict([('Fst', '')]),
                                     'head': 7,
                                     'id': 8,
                                     'lemma': '.',
                                     'misc': None,
                                     'upostag': 'Z',
                                     'xpostag': 'Z'}],
                    'base_span': (46, 47)},
                   {'annotations': [{'deprel': '@SUBJ',
                                     'deps': None,
                                     'feats': OrderedDict([('ps3', ''),
                                                           ('sg', ''),
                                                           ('nom', '')]),
                                     'head': 2,
                                     'id': 1,
                                     'lemma': 'tema',
                                     'misc': None,
                                     'upostag': 'P',
                                     'xpostag': 'Ppers'}],
                    'base_span': (48, 50)},
                   {'annotations': [{'deprel': 'ROOT',
                                     'deps': None,
                                     'feats': OrderedDict([('indic', ''),
                                                           ('pres', ''),
                                                           ('ps3', ''),
                                                           ('sg', '')]),
                                     'head': 0,
                                     'id': 2,
                                     'lemma': 'ole',
                                     'misc': None,
                                     'upostag': 'V',
                                     'xpostag': 'V'}],
                    'base_span': (51, 53)},
                   {'annotations': [{'deprel': '@NN>',
                                     'deps': None,
                                     'feats': OrderedDict([('pos', ''),
                                                           ('det', ''),
                                                           ('refl', ''),
                                                           ('sg', ''),
                                                           ('nom', '')]),
                                     'head': 4,
                                     'id': 3,
                                     'lemma': 'ise',
                                     'misc': None,
                                     'upostag': 'P',
                                     'xpostag': 'P'}],
                    'base_span': (54, 57)},
                   {'annotations': [{'deprel': '@PRD',
                                     'deps': None,
                                     'feats': OrderedDict([('sg', ''), ('nom', '')]),
                                     'head': 2,
                                     'id': 4,
                                     'lemma': 'tee',
                                     'misc': None,
                                     'upostag': 'S',
                                     'xpostag': 'S'}],
                    'base_span': (58, 61)},
                   {'annotations': [{'deprel': '@AN>',
                                     'deps': None,
                                     'feats': OrderedDict([('ord', ''),
                                                           ('sg', ''),
                                                           ('ad', ''),
                                                           ('l', '')]),
                                     'head': 6,
                                     'id': 5,
                                     'lemma': 'esimene',
                                     'misc': None,
                                     'upostag': 'N',
                                     'xpostag': 'A'}],
                    'base_span': (62, 70)},
                   {'annotations': [{'deprel': '@ADVL',
                                     'deps': None,
                                     'feats': OrderedDict([('sg', ''), ('ad', '')]),
                                     'head': 2,
                                     'id': 6,
                                     'lemma': 'pool',
                                     'misc': None,
                                     'upostag': 'S',
                                     'xpostag': 'S'}],
                    'base_span': (71, 77)},
                   {'annotations': [{'deprel': '@Punc',
                                     'deps': None,
                                     'feats': OrderedDict([('Fst', '')]),
                                     'head': 6,
                                     'id': 7,
                                     'lemma': '.',
                                     'misc': None,
                                     'upostag': 'Z',
                                     'xpostag': 'Z'}],
                    'base_span': (77, 78)},
                   {'annotations': [{'deprel': '@AN>',
                                     'deps': None,
                                     'feats': OrderedDict([('sg', ''), ('nom', '')]),
                                     'head': 2,
                                     'id': 1,
                                     'lemma': 'valge',
                                     'misc': None,
                                     'upostag': 'A',
                                     'xpostag': 'A'}],
                    'base_span': (79, 84)},
                   {'annotations': [{'deprel': '@SUBJ',
                                     'deps': None,
                                     'feats': OrderedDict([('sg', ''), ('nom', '')]),
                                     'head': 3,
                                     'id': 2,
                                     'lemma': 'jänes',
                                     'misc': None,
                                     'upostag': 'S',
                                     'xpostag': 'S'}],
                    'base_span': (85, 90)},
                   {'annotations': [{'deprel': 'ROOT',
                                     'deps': None,
                                     'feats': OrderedDict([('indic', ''),
                                                           ('impf', ''),
                                                           ('ps3', ''),
                                                           ('sg', '')]),
                                     'head': 0,
                                     'id': 3,
                                     'lemma': 'jooks',
                                     'misc': None,
                                     'upostag': 'V',
                                     'xpostag': 'V'}],
                    'base_span': (91, 98)},
                   {'annotations': [{'deprel': '@ADVL',
                                     'deps': None,
                                     'feats': OrderedDict([('sg', ''), ('adit', '')]),
                                     'head': 3,
                                     'id': 4,
                                     'lemma': 'mets',
                                     'misc': None,
                                     'upostag': 'S',
                                     'xpostag': 'S'}],
                    'base_span': (99, 104)},
                   {'annotations': [{'deprel': '@Punc',
                                     'deps': None,
                                     'feats': OrderedDict([('Exc', '')]),
                                     'head': 4,
                                     'id': 5,
                                     'lemma': '!',
                                     'misc': None,
                                     'upostag': 'Z',
                                     'xpostag': 'Z'}],
                    'base_span': (104, 105)}]}
    tagger = MaltParserTagger()
    tagger.tag( text )
    #from pprint import pprint
    #pprint( layer_to_dict(text.maltparser_syntax) )
    assert expected_layer_dict == layer_to_dict( text.maltparser_syntax )
    
    simpler_output = simplify_syntax_layer( text.maltparser_syntax )
    #from pprint import pprint
    #pprint( simpler_output )
    assert simpler_output == \
        [('Ilus', 'A', '@AN>', 1, 4),
         ('suur', 'A', '@AN>', 2, 4),
         ('karvane', 'A', '@AN>', 3, 4),
         ('kass', 'S', '@SUBJ', 4, 5),
         ('nurrus', 'V', 'ROOT', 5, 0),
         ('punasel', 'A', '@AN>', 6, 7),
         ('diivanil', 'S', '@ADVL', 7, 5),
         ('.', 'Z', '@Punc', 8, 7),
         ('Ta', 'P', '@SUBJ', 1, 2),
         ('on', 'V', 'ROOT', 2, 0),
         ('ise', 'P', '@NN>', 3, 4),
         ('tee', 'S', '@PRD', 4, 2),
         ('esimesel', 'N', '@AN>', 5, 6),
         ('poolel', 'S', '@ADVL', 6, 2),
         ('.', 'Z', '@Punc', 7, 6),
         ('Valge', 'A', '@AN>', 1, 2),
         ('jänes', 'S', '@SUBJ', 2, 3),
         ('jooksis', 'V', 'ROOT', 3, 0),
         ('metsa', 'S', '@ADVL', 4, 3),
         ('!', 'Z', '@Punc', 5, 4) ]

    # Case 2: rerun the same parser on different text
    text2 = Text('Ja vana karu lõi suurt trummi.').tag_layer(['morph_extended'])
    conll_morph_tagger.tag( text2 )
    assert 'conll_morph' in text2.layers
    tagger.tag( text2 )
    #from pprint import pprint
    #pprint( layer_to_dict(text2.maltparser_syntax) )
    expected_layer_dict_2 = \
        {'ambiguous': False,
         'attributes': ('id',
                        'lemma',
                        'upostag',
                        'xpostag',
                        'feats',
                        'head',
                        'deprel',
                        'deps',
                        'misc',
                        'parent_span',
                        'children'),
         'enveloping': None,
         'meta': {},
         'name': 'maltparser_syntax',
         'parent': None,
         'serialisation_module': 'syntax_v0',
         'spans': [{'annotations': [{'deprel': '@J',
                                     'deps': None,
                                     'feats': None,
                                     'head': 4,
                                     'id': 1,
                                     'lemma': 'ja',
                                     'misc': None,
                                     'upostag': 'J',
                                     'xpostag': 'Jc'}],
                    'base_span': (0, 2)},
                   {'annotations': [{'deprel': '@AN>',
                                     'deps': None,
                                     'feats': OrderedDict([('sg', ''), ('nom', '')]),
                                     'head': 3,
                                     'id': 2,
                                     'lemma': 'vana',
                                     'misc': None,
                                     'upostag': 'A',
                                     'xpostag': 'A'}],
                    'base_span': (3, 7)},
                   {'annotations': [{'deprel': '@SUBJ',
                                     'deps': None,
                                     'feats': OrderedDict([('sg', ''), ('nom', '')]),
                                     'head': 4,
                                     'id': 3,
                                     'lemma': 'karu',
                                     'misc': None,
                                     'upostag': 'S',
                                     'xpostag': 'S'}],
                    'base_span': (8, 12)},
                   {'annotations': [{'deprel': 'ROOT',
                                     'deps': None,
                                     'feats': OrderedDict([('indic', ''),
                                                           ('impf', ''),
                                                           ('ps3', ''),
                                                           ('sg', '')]),
                                     'head': 0,
                                     'id': 4,
                                     'lemma': 'loo',
                                     'misc': None,
                                     'upostag': 'V',
                                     'xpostag': 'V'}],
                    'base_span': (13, 16)},
                   {'annotations': [{'deprel': '@AN>',
                                     'deps': None,
                                     'feats': OrderedDict([('sg', ''), ('part', '')]),
                                     'head': 6,
                                     'id': 5,
                                     'lemma': 'suur',
                                     'misc': None,
                                     'upostag': 'A',
                                     'xpostag': 'A'}],
                    'base_span': (17, 22)},
                   {'annotations': [{'deprel': '@OBJ',
                                     'deps': None,
                                     'feats': OrderedDict([('sg', ''), ('gen', '')]),
                                     'head': 4,
                                     'id': 6,
                                     'lemma': 'trumm',
                                     'misc': None,
                                     'upostag': 'S',
                                     'xpostag': 'S'}],
                    'base_span': (23, 29)},
                   {'annotations': [{'deprel': '@Punc',
                                     'deps': None,
                                     'feats': OrderedDict([('Fst', '')]),
                                     'head': 6,
                                     'id': 7,
                                     'lemma': '.',
                                     'misc': None,
                                     'upostag': 'Z',
                                     'xpostag': 'Z'}],
                    'base_span': (29, 30)}]}
    assert expected_layer_dict_2 == layer_to_dict( text2.maltparser_syntax )

