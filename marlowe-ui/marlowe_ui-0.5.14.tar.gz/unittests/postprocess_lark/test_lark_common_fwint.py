import unittest
from parameterized import parameterized

import lark

from marlowe_ui.postprocess_lark import lark_common

# parse "'Cascade',I6,':',5X,'Group',I5,6X,'Number',I3" collectly
# Cascade     2:     Group    1      Number  2

grammar = '''\
        cascade: "Cascade" fwint6 ":" _SS~5 "Group" fwint5 _SS~6 "Number" fwint3 _NL'''

grammar += lark_common.grammar + lark_common.grammar_fixedwidth_int 

class Transformer(lark_common.Transformer):
    def __init__(self):
        super().__init__()

    def cascade(self, args):
        # cascade: "Cascade" fwint6 ":" _SS~5 "Group" fwint5 _SS~6 "Number" fwint3 _NL
        return {
                'Cascade':args[0],
                'Group':args[1],
                'Number':args[2]
                }

class Parser():
    def __init__(self):
        self.transformer = Transformer()
        self.parser = lark.Lark(grammar=grammar, parser='lalr',
                transformer=self.transformer,
                start='cascade')


    def parse(self, text):
        return self.parser.parse(text)



class TestLarkCommonFwint(unittest.TestCase):
    def setUp(self):
        self.parser = Parser()


    @parameterized.expand([
        ('Cascade     2:     Group    1      Number  2\n',
            {'Cascade':2, 'Group':1, 'Number':2}),
        ('Cascade     2:     Group    1      Number***\n',
            {'Cascade':2, 'Group':1, 'Number':999}),
        ('Cascade999999:     Group11111      Number  0\n',
            {'Cascade':999999, 'Group':11111, 'Number':0}),
        ('Cascade    -1:     Group    1      Number  0\n',
            {'Cascade':-1, 'Group':1, 'Number':0}),
        ('Cascade-99999:     Group    1      Number  0\n',
            {'Cascade':-99999, 'Group':1, 'Number':0}),
        ('Cascade -99999:     Group    1      Number  0\n',
            {'Cascade':-99999, 'Group':1, 'Number':0}),
        ('Cascade    -9999999:     Group    1      Number  0\n',
            {'Cascade':-9999999, 'Group':1, 'Number':0}),
        ])
    def test_lark_common_fwint(self, in_, out):
        result = self.parser.parse(in_)
        self.assertEqual(result, out)
