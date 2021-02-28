import unittest

from .args import parse_args


def args_to_dict(args):
    return {var_name: getattr(args, var_name) for var_name in vars(args)}


class TestArgs(unittest.TestCase):
    def test_together(self):
        args, inputs = parse_args(['./dplot.py', 'output.png', '--crysol', 'in/crysol.int', '--psaxs',
                                   'in/psaxs.tsv', '--log'])

        self.assertEqual(args_to_dict(args), {
            'output': 'output.png', 'title': None, 'log': True, 'x': 'Q', 'y': None, 'x_label': None, 'y_label': None,
            'verbose': False
        })

        self.assertEqual(len(inputs), 2)

        self.assertEqual(args_to_dict(inputs[0]), {
            'crysol': 'in/crysol.int', 'psaxs': None, 'debyer': None, 'other': None, 'skip': 1,
            'headers': 'Q,Intensity,Scattering (in vacuo),Scattering (excluded volume),Convex border layer',
            'input': 'in/crysol.int'
        })

        self.assertEqual(args_to_dict(inputs[1]), {
            'crysol': None, 'psaxs': 'in/psaxs.tsv', 'debyer': None, 'other': None, 'skip': None,
            'headers': 'Q,Intensity', 'input': 'in/psaxs.tsv'
        })
