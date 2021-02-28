"""
chatrelater.visualization_cli
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Command line interface for visualizer.

:Copyright: 2007-2021 Jochen Kupperschmidt
:License: MIT, see LICENSE for details.
"""

from argparse import ArgumentParser
from pathlib import Path

from graphviz.backend import ENGINES, FORMATS

from .nicknames import Nickname
from .serialization import load_data
from .visualization import (
    DEFAULT_FORMAT,
    DEFAULT_PROGRAM,
    generate_dot,
    write_file,
)


def parse_args():
    """Setup and apply the command line parser."""
    parser = ArgumentParser()

    parser.add_argument(
        '-f',
        '--format',
        dest='format',
        default=DEFAULT_FORMAT,
        choices=sorted(FORMATS),
        help='output format supported by GraphViz (default: {})'.format(
            DEFAULT_FORMAT
        ),
    )

    parser.add_argument(
        '-p',
        '--program',
        dest='program',
        default=DEFAULT_PROGRAM,
        choices=sorted(ENGINES),
        help='GraphViz program to create output with (default: {})'.format(
            DEFAULT_PROGRAM
        ),
    )

    parser.add_argument('input_filename', metavar='INPUT_FILENAME')

    parser.add_argument(
        'output_filename_prefix', metavar='OUTPUT_FILENAME_PREFIX'
    )

    return parser.parse_args()


def main() -> None:
    args = parse_args()
    input_filename = Path(args.input_filename)

    loaded_nicknames, loaded_relations, directed = load_data(input_filename)
    nicknames = [Nickname(nick) for nick in loaded_nicknames]
    relations = [
        (Nickname(nick1), Nickname(nick2), count)
        for nick1, nick2, count in loaded_relations
    ]

    dot = generate_dot(
        nicknames,
        relations,
        name=args.output_filename_prefix,
        format=args.format,
        program=args.program,
        directed=directed,
    )

    write_file(dot)
