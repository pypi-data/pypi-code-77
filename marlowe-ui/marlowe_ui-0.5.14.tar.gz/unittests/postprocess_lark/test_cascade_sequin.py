import unittest
from parameterized import parameterized

import pathlib

from marlowe_ui.postprocess_lark import cascade_sequin

class TestCascadeSequin(unittest.TestCase):
    def setUp(self):
        self.current_dir = pathlib.Path(__file__).parent

    # input files are at final_sequex_examples/
    @parameterized.expand([
        '01.cascade_sequin.txt',
        '02.cascade_sequin.txt',
        '03.cascade_sequin.txt',
        ])
    def test_final_sequex(self, filename):
        p = self.current_dir / 'cascade_sequin_examples'/ filename
        # print(p)
        # final_sequex.parse(text)
        with p.open('rt') as f:
            result = cascade_sequin.parse(f.read())
