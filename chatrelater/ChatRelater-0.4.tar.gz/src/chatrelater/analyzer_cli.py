"""
chatrelater.analyzer_cli
~~~~~~~~~~~~~~~~~~~~~~~~

Command line interface for analyzer.

:Copyright: 2007-2021 Jochen Kupperschmidt
:License: MIT, see LICENSE for details.
"""

from argparse import ArgumentParser
from pathlib import Path

from .analyzer import analyze
from .serialization import serialize_data_to_file, serialize_data_to_stdout


def parse_args():
    """Setup and apply the command line parser."""
    parser = ArgumentParser()

    parser.add_argument(
        '-d',
        '--directed',
        action='store_true',
        dest='directed',
        help='preserve directed relations instead of unifying them',
    )

    parser.add_argument(
        '-n',
        '--no-unrelated-nicknames',
        action='store_true',
        dest='no_unrelated_nicknames',
        help='exclude unrelated nicknames to avoid unconnected nodes to be drawn',
    )

    parser.add_argument(
        '-o',
        '--output-filename',
        dest='output_filename',
        help='save the output to this file (default: write to STDOUT)',
    )

    parser.add_argument(
        '-v',
        '--verbose',
        action='store_true',
        dest='verbose',
        help='display the resulting relations',
    )

    parser.add_argument('filenames', metavar='FILENAME', nargs='+')

    return parser.parse_args()


def main() -> None:
    args = parse_args()
    filenames = [Path(fn) for fn in args.filenames]
    if args.output_filename is not None:
        output_filename = Path(args.output_filename)
    else:
        output_filename = None

    # Analyze data.
    nicknames, relations = analyze(
        filenames,
        directed=args.directed,
        no_unrelated_nicknames=args.no_unrelated_nicknames,
    )

    # Show details.
    if args.verbose:
        connection_template = '%3dx %s <-> %s'
        if args.directed:
            connection_template = connection_template.replace('<', '')
        print()
        for rel in sorted(relations, key=lambda x: str.lower(x[0])):
            print(connection_template % (rel[2], rel[0], rel[1]))
        print()
        print(
            'Found {len(nicknames):d} nicknames in {len(relations):d} relations.'
        )

    # Store result.
    data = {
        'nicknames': list(nicknames),
        'relations': relations,
        'directed': args.directed,
    }
    if output_filename is not None:
        serialize_data_to_file(data, output_filename)
    else:
        serialize_data_to_stdout(data)
