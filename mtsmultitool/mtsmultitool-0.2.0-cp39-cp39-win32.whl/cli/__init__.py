import sys
import argparse
import textwrap

from .. import __version__
from . import device_cli as device


def create_parser():
    desc = textwrap.dedent(f'''Multitool Utility - Version {__version__} - MultiTech Systems Inc.\
            ''')
    top_parser = argparse.ArgumentParser(
        prog='multitool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=desc)
    subparsers = top_parser.add_subparsers(metavar='CMD')

    top_parser.add_argument('-v', '--version', action='version', version=f'%(prog)s {__version__}', help='Print version information')

    device.add_parser(subparsers)

    return top_parser


def main():
    parser = create_parser()
    if len(sys.argv) == 1:
        parser.print_help()
    else:
        args = parser.parse_args()
        try:
            args.func(args)
        except AttributeError:
            pass


if __name__ == '__main__':
    main()

