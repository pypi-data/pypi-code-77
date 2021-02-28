"""
chatrelater.analyzer
~~~~~~~~~~~~~~~~~~~~

Analyze (not necessarily only) IRC logfiles and determine relations
between chat users.

So far, only logfiles produced by XChat_ were tested.

For a line to be recognized, it has to start with a nickname in angle
brackets, followed by a space (e. g. `<SomeUser23> hey what's up?`).

Also, users are expected to use the nickname autocompletion feature, so
only exact nicknames with matching case are recognized.

.. _XChat: http://www.xchat.org/

:Copyright: 2007-2021 Jochen Kupperschmidt
:License: MIT, see LICENSE for details.
"""

from pathlib import Path
from typing import Iterable, Iterator, List, Set, Tuple

from .nicknames import clean_nickname, Nickname, NicknameRegistry


def iter_files(filenames: Iterable[Path]) -> Iterator[str]:
    """Yield lines from multiple files."""
    for fn in filenames:
        with fn.open() as f:
            for line in f:
                yield line


def parse_logfile(
    lines: Iterable[str],
) -> Tuple[Set[Nickname], List[Tuple[Nickname, str]]]:
    """Return a set of nicknames and a list of (nickname, message) tuples
    extracted from the given lines.
    """
    nicknames: Set[Nickname] = set()
    loglines: List[Tuple[Nickname, str]] = []

    for nickname, message in parse_log(lines):
        nicknames.add(nickname)
        loglines.append((nickname, message))

    return nicknames, loglines


def parse_log(lines: Iterable[str]) -> Iterator[Tuple[Nickname, str]]:
    """Select relevant lines and split each of those into a
    (nickname, message) pair.
    """
    for line in lines:
        # Skip everything that is not a public (or query) message
        # (joins, parts, modes, notices etc.).
        if not line.startswith('<'):
            continue

        try:
            nickname, message = line[1:].strip().split('> ', 1)
            nickname = clean_nickname(nickname)
            yield nickname, message
        except ValueError:
            pass


def relate_nicknames(
    nicknames: Set[Nickname], loglines: Iterable[Tuple[Nickname, str]]
) -> Iterator[Tuple[Nickname, Nickname]]:
    """Try to figure out relations between users.

    Line beginnings are checked to find textual references between users.
    """
    nickname_registry = NicknameRegistry(nicknames)

    for author_nickname, message in loglines:
        addressed_nickname = message.split(' ', 1)[0].strip(':,.?!@')
        matching_addressed_nickname = nickname_registry.find(addressed_nickname)
        if matching_addressed_nickname:
            yield author_nickname, matching_addressed_nickname


def compress_relations(
    relations: Iterable[Tuple[Nickname, Nickname]], *, unify: bool = False
) -> Iterator[Tuple[Nickname, Nickname, int]]:
    """Combine one or more equal (nick1, nick2) tuples into a single
    (nick1, nick2, count) tuple.

    If ``unify`` is true, relations with identic items in different order
    will be put in the same order so they are equal.
    """
    if unify:
        relations_list = [tuple(sorted(rel)) for rel in relations]
    else:
        relations_list = list(relations)

    for rel in set(relations_list):
        yield rel[0], rel[1], relations_list.count(rel)


def analyze(
    filenames: List[Path],
    *,
    directed: bool = False,
    no_unrelated_nicknames: bool = False,
) -> Tuple[Set[Nickname], List[Tuple[Nickname, Nickname, int]]]:
    """Parse logfiles and return nicknames and their determined relations."""
    nicknames, loglines = parse_logfile(iter_files(filenames))
    relations = relate_nicknames(nicknames, loglines)
    compressed_relations = list(
        compress_relations(relations, unify=not directed)
    )

    if no_unrelated_nicknames:
        nicknames = set()
        for rel in compressed_relations:
            nicknames.update(rel[:2])

    return nicknames, compressed_relations
