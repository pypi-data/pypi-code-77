import pytest

from estnltk import Text
from estnltk.converters import dict_to_layer
from estnltk.taggers import VislTagger

from estnltk.taggers.syntax.vislcg3_syntax import check_if_vislcg_is_in_path

visl_dict = {
    'name': 'visl',
    'attributes': ('id',
                   'lemma',
                   'ending',
                   'partofspeech',
                   'subtype',
                   'mood',
                   'tense',
                   'voice',
                   'person',
                   'inf_form',
                   'number',
                   'case',
                   'polarity',
                   'number_format',
                   'capitalized',
                   'finiteness',
                   'subcat',
                   'clause_boundary',
                   'deprel',
                   'head'),
    'parent': 'morph_extended',
    'enveloping': None,
    'ambiguous': True,
    'serialisation_module': None,
    'meta': {},
    'spans': [{'base_span': (0, 4),
               'annotations': [{'person': '_',
                                'number': '_',
                                'finiteness': '_',
                                'tense': '_',
                                'partofspeech': 'D',
                                'voice': '_',
                                'polarity': '_',
                                'subtype': '_',
                                'deprel': '@ADVL',
                                'ending': '0',
                                'capitalized': 'cap',
                                'lemma': 'juba',
                                'id': 1,
                                'subcat': '_',
                                'inf_form': '_',
                                'clause_boundary': '_',
                                'mood': '_',
                                'head': 3,
                                'case': '_',
                                'number_format': '_'}]},
              {'base_span': (5, 10),
               'annotations': [{'person': 'ps3',
                                'number': 'sg',
                                'finiteness': '_',
                                'tense': 'pres',
                                'partofspeech': 'V',
                                'voice': 'ps',
                                'polarity': 'af',
                                'subtype': 'main',
                                'deprel': '@FMV',
                                'ending': 'b',
                                'capitalized': '_',
                                'lemma': 'taht',
                                'id': 2,
                                'subcat': '_',
                                'inf_form': '_',
                                'clause_boundary': '_',
                                'mood': 'indic',
                                'head': 0,
                                'case': '_',
                                'number_format': '_'}]},
              {'base_span': (11, 16),
               'annotations': [{'person': '_',
                                'number': '_',
                                'finiteness': '_',
                                'tense': '_',
                                'partofspeech': 'V',
                                'voice': '_',
                                'polarity': '_',
                                'subtype': 'main',
                                'deprel': '@OBJ',
                                'ending': 'da',
                                'capitalized': '_',
                                'lemma': 'saa',
                                'id': 3,
                                'subcat': '_',
                                'inf_form': 'inf',
                                'clause_boundary': '_',
                                'mood': '_',
                                'head': 2,
                                'case': '_',
                                'number_format': '_'}]},
              {'base_span': (17, 25),
               'annotations': [{'person': '_',
                                'number': 'sg',
                                'finiteness': '_',
                                'tense': '_',
                                'partofspeech': 'S',
                                'voice': '_',
                                'polarity': '_',
                                'subtype': 'com',
                                'deprel': '@ADVL',
                                'ending': 'ks',
                                'capitalized': '_',
                                'lemma': 'pagar',
                                'id': 4,
                                'subcat': '_',
                                'inf_form': '_',
                                'clause_boundary': '_',
                                'mood': '_',
                                'head': 3,
                                'case': 'tr',
                                'number_format': '_'}]},
              {'base_span': (25, 26),
               'annotations': [{'person': '_',
                                'number': '_',
                                'finiteness': '_',
                                'tense': '_',
                                'partofspeech': 'Z',
                                'voice': '_',
                                'polarity': '_',
                                'subtype': 'Exc',
                                'deprel': '_',
                                'ending': '_',
                                'capitalized': '_',
                                'lemma': '!',
                                'id': 5,
                                'subcat': '_',
                                'inf_form': '_',
                                'clause_boundary': 'CLB',
                                'mood': '_',
                                'head': 4,
                                'case': '_',
                                'number_format': '_'}]},
              {'base_span': (27, 30),
               'annotations': [{'person': '_',
                                'number': 'pl',
                                'finiteness': '_',
                                'tense': '_',
                                'partofspeech': 'P',
                                'voice': '_',
                                'polarity': '_',
                                'subtype': ['pos', 'det', 'refl'],
                                'deprel': '@ADVL',
                                'ending': '0',
                                'capitalized': 'cap',
                                'lemma': 'ise',
                                'id': 1,
                                'subcat': '_',
                                'inf_form': '_',
                                'clause_boundary': '_',
                                'mood': '_',
                                'head': 3,
                                'case': 'nom',
                                'number_format': '_'},
                               {'person': '_',
                                'number': 'sg',
                                'finiteness': '_',
                                'tense': '_',
                                'partofspeech': 'P',
                                'voice': '_',
                                'polarity': '_',
                                'subtype': ['pos', 'det', 'refl'],
                                'deprel': '@ADVL',
                                'ending': '0',
                                'capitalized': 'cap',
                                'lemma': 'ise',
                                'id': 1,
                                'subcat': '_',
                                'inf_form': '_',
                                'clause_boundary': '_',
                                'mood': '_',
                                'head': 3,
                                'case': 'nom',
                                'number_format': '_'}]},
              {'base_span': (31, 36),
               'annotations': [{'person': '_',
                                'number': '_',
                                'finiteness': '_',
                                'tense': '_',
                                'partofspeech': 'D',
                                'voice': '_',
                                'polarity': '_',
                                'subtype': '_',
                                'deprel': '@ADVL',
                                'ending': '0',
                                'capitalized': '_',
                                'lemma': 'alles',
                                'id': 2,
                                'subcat': '_',
                                'inf_form': '_',
                                'clause_boundary': '_',
                                'mood': '_',
                                'head': 3,
                                'case': '_',
                                'number_format': '_'}]},
              {'base_span': (37, 40),
               'annotations': [{'person': '_',
                                'number': 'sg',
                                'finiteness': '_',
                                'tense': '_',
                                'partofspeech': 'S',
                                'voice': '_',
                                'polarity': '_',
                                'subtype': 'com',
                                'deprel': '@NN>',
                                'ending': '0',
                                'capitalized': '_',
                                'lemma': 'tee',
                                'id': 3,
                                'subcat': '_',
                                'inf_form': '_',
                                'clause_boundary': '_',
                                'mood': '_',
                                'head': 0,
                                'case': 'gen',
                                'number_format': '_'},
                               {'person': '_',
                                'number': 'sg',
                                'finiteness': '_',
                                'tense': '_',
                                'partofspeech': 'S',
                                'voice': '_',
                                'polarity': '_',
                                'subtype': 'com',
                                'deprel': '@OBJ',
                                'ending': '0',
                                'capitalized': '_',
                                'lemma': 'tee',
                                'id': 3,
                                'subcat': '_',
                                'inf_form': '_',
                                'clause_boundary': '_',
                                'mood': '_',
                                'head': 0,
                                'case': 'gen',
                                'number_format': '_'}]},
              {'base_span': (41, 49),
               'annotations': [{'person': '_',
                                'number': 'sg',
                                'finiteness': '_',
                                'tense': '_',
                                'partofspeech': 'N',
                                'voice': '_',
                                'polarity': '_',
                                'subtype': 'ord',
                                'deprel': '@AN>',
                                'ending': 'l',
                                'capitalized': '_',
                                'lemma': 'esimene',
                                'id': 4,
                                'subcat': '_',
                                'inf_form': '_',
                                'clause_boundary': '_',
                                'mood': '_',
                                'head': 5,
                                'case': 'ad',
                                'number_format': 'l'}]},
              {'base_span': (50, 56),
               'annotations': [{'person': '_',
                                'number': 'sg',
                                'finiteness': '_',
                                'tense': '_',
                                'partofspeech': 'S',
                                'voice': '_',
                                'polarity': '_',
                                'subtype': 'com',
                                'deprel': ['@<NN', '@ADVL'],
                                'ending': 'l',
                                'capitalized': '_',
                                'lemma': 'pool',
                                'id': 5,
                                'subcat': '_',
                                'inf_form': '_',
                                'clause_boundary': '_',
                                'mood': '_',
                                'head': 3,
                                'case': 'ad',
                                'number_format': '_'}]},
              {'base_span': (57, 58),
               'annotations': [{'person': '_',
                                'number': '_',
                                'finiteness': '_',
                                'tense': '_',
                                'partofspeech': 'Z',
                                'voice': '_',
                                'polarity': '_',
                                'subtype': 'Com',
                                'deprel': '_',
                                'ending': '_',
                                'capitalized': '_',
                                'lemma': ',',
                                'id': 6,
                                'subcat': '_',
                                'inf_form': '_',
                                'clause_boundary': '_',
                                'mood': '_',
                                'head': 5,
                                'case': '_',
                                'number_format': '_'}]},
              {'base_span': (59, 64),
               'annotations': [{'person': '_',
                                'number': '_',
                                'finiteness': '_',
                                'tense': '_',
                                'partofspeech': 'D',
                                'voice': '_',
                                'polarity': '_',
                                'subtype': '_',
                                'deprel': '@ADVL',
                                'ending': '0',
                                'capitalized': '_',
                                'lemma': 'vaevu',
                                'id': 7,
                                'subcat': '_',
                                'inf_form': '_',
                                'clause_boundary': '_',
                                'mood': '_',
                                'head': 3,
                                'case': '_',
                                'number_format': '_'}]},
              {'base_span': (65, 82),
               'annotations': [{'person': '_',
                                'number': 'sg',
                                'finiteness': '_',
                                'tense': '_',
                                'partofspeech': 'A',
                                'voice': '_',
                                'polarity': '_',
                                'subtype': 'pos',
                                'deprel': '@ADVL',
                                'ending': '0',
                                'capitalized': '_',
                                'lemma': 'kolme_kümne_kolmene',
                                'id': 8,
                                'subcat': '_',
                                'inf_form': '_',
                                'clause_boundary': '_',
                                'mood': '_',
                                'head': 5,
                                'case': 'nom',
                                'number_format': '_'}]},
              {'base_span': (83, 84),
               'annotations': [{'person': '_',
                                'number': '_',
                                'finiteness': '_',
                                'tense': '_',
                                'partofspeech': 'Z',
                                'voice': '_',
                                'polarity': '_',
                                'subtype': 'Fst',
                                'deprel': '_',
                                'ending': '_',
                                'capitalized': '_',
                                'lemma': '.',
                                'id': 9,
                                'subcat': '_',
                                'inf_form': '_',
                                'clause_boundary': 'CLB',
                                'mood': '_',
                                'head': 8,
                                'case': '_',
                                'number_format': '_'}]}]}


@pytest.mark.skipif(not check_if_vislcg_is_in_path('vislcg3'),
                    reason="a directory containing vislcg3 executable must be inside the system PATH")
def test_visl_tagger():
    text = Text('Juba tahab saada pagariks! Ise alles tee esimesel poolel , vaevu kolmekümnekolmene .').tag_layer(
            ['morph_extended'])

    tagger = VislTagger()
    tagger.tag(text)
    assert dict_to_layer(visl_dict) == text.visl, text.visl.diff(dict_to_layer(visl_dict))
