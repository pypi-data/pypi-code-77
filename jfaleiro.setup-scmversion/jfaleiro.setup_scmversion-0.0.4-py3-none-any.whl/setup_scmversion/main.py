#
#     setup_scmversion - Builds a pythonic version number based on scm tags
#                        and branches.
#
#     Copyright (C) 2019 Jorge M. Faleiro Jr.
#
#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU Affero General Public License as published
#     by the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU Affero General Public License for more details.
#
#     You should have received a copy of the GNU Affero General Public License
#     along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
import argparse
import sys

from .parser import (DEFAULT_VERSION_FILE, Tags, check_tag, parser_factory,
                     parsers, show_tagged, tag_version)


def main(args=sys.argv[1:]):
    version_parser = parser_factory()
    commands = {
        'version':
            lambda _: version_parser.version(),
        'version-type':
            lambda _: version_parser.version_type().name,
        'parsers':
            lambda _: parsers(),
        'tag-version':
            lambda args: "tagged " + str(
                tag_version(package=args.package, file=args.file,
                            pre_commit=args.pre_commit)),
        'show':
            lambda args: "tagged " + str(
                show_tagged(package=args.package, file=args.file)),
        'check':
            lambda args: "OK " + str(
                show_tagged(package=args.package, file=args.file)
            ) if check_tag(
                package=args.package, file=args.file) is None else ""
    }

    parser = argparse.ArgumentParser(description='Version parser from scm')
    sub_parsers = parser.add_subparsers(required=True, dest='command')

    sub_parsers.add_parser(
        'version',
        help='displays the version'
    )

    sub_parsers.add_parser(
        'version-type',
        help=f'displays the version type (one of {[e.name for e in Tags]})'
    )
    sub_parsers.add_parser(
        'parsers',
        help='lists all parsers available'
    )

    tag_parser = sub_parsers.add_parser(
        'tag-version',
        help='tag the package with the version')
    tag_parser_group = tag_parser.add_mutually_exclusive_group()
    tag_parser_group.add_argument(
        '--auto',
        help='autodetect package name',
        action='store_true')
    tag_parser_group.add_argument(
        'package', nargs='?',
        help='name of the package')
    tag_parser.add_argument(
        '--pre-commit',
        help=('anticipates (increments by one) the '
              'number of commits during a pre-commit operation'),
        action='store_true'
    )
    tag_parser.add_argument(
        'file',
        help='name of the file',
        nargs='?',
        default=DEFAULT_VERSION_FILE)

    show_tags_parser = sub_parsers.add_parser(
        'show',
        help='show what is currently tagged'
    )
    show_tags_parser_group = show_tags_parser.add_mutually_exclusive_group()
    show_tags_parser_group.add_argument(
        '--auto',
        help='autodetect package name',
        action='store_true')
    show_tags_parser_group.add_argument(
        'package', nargs='?',
        help='name of the package')
    show_tags_parser.add_argument(
        'file',
        help='name of the file',
        nargs='?',
        default=DEFAULT_VERSION_FILE)

    check_tags_parser = sub_parsers.add_parser(
        'check',
        help='asserts versions on version file and scm are the same'
    )
    check_tags_parser_group = check_tags_parser.add_mutually_exclusive_group()
    check_tags_parser_group.add_argument(
        '--auto',
        help='autodetect package name',
        action='store_true')
    check_tags_parser_group.add_argument(
        'package', nargs='?',
        help='name of the package')
    check_tags_parser.add_argument(
        'file',
        help='name of the file',
        nargs='?',
        default=DEFAULT_VERSION_FILE)
    args = parser.parse_args(args)
    print(commands[args.command](args))


if __name__ == "__main__":  # pragma: no cover
    main(sys.argv[1:])
