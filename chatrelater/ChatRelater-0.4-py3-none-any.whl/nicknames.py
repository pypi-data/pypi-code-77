"""
chatrelater.nicknames
~~~~~~~~~~~~~~~~~~~~~

:Copyright: 2007-2021 Jochen Kupperschmidt
:License: MIT, see LICENSE for details.
"""

from typing import Iterable, NewType, Optional


Nickname = NewType('Nickname', str)


STATUS_SYMBOLS = frozenset('@%+')


def clean_nickname(nickname: str) -> Nickname:
    """Remove potential status symbol in front of nickname.

    Symbols that will be removed are:

    - `@` ("op")
    - `%` ("halfop")
    - `+` ("voice")
    """
    if nickname[0] in STATUS_SYMBOLS:
        base_nickname = nickname[1:]
    else:
        base_nickname = nickname

    return Nickname(base_nickname)


class NicknameRegistry(object):
    def __init__(self, nicknames: Iterable[Nickname]) -> None:
        self.nicknames = frozenset(nicknames)
        self._case_insensitive_index = {
            remove_case(nickname): nickname for nickname in nicknames
        }

    def find(self, nickname_candidate: str) -> Optional[Nickname]:
        """Try to case-insensitively match the nickname and return the
        original spelling (or `None` if not matching).
        """
        return self._case_insensitive_index.get(remove_case(nickname_candidate))


def remove_case(nickname_candidate: str) -> Nickname:
    return Nickname(nickname_candidate.lower())
