import os
import subprocess
from typing import Set

from ..core.log import log
from .path import get_relative_path_if_in_cwd


def get_root_directory() -> str:
    """
    :raises: CalledProcessError
    """
    return subprocess.check_output(
        'git rev-parse --show-toplevel'.split(),
    ).decode('utf-8').strip()


def get_tracked_files(root: str) -> Set[str]:
    """Parsing .gitignore rules is hard.

    However, a way we can get around this problem by just listing all
    currently tracked git files, and start our search from there.
    After all, if it isn't in the git repo, we're not concerned about
    it, because secrets aren't being entered in a shared place.

    :raises: CalledProcessError
    """
    output = set([])
    try:
        files = subprocess.check_output(
            ['git', '-C', root, 'ls-files'],
            stderr=subprocess.DEVNULL,
        )

        for filename in files.decode('utf-8').splitlines():
            path = get_relative_path_if_in_cwd(os.path.join(root, filename))
            if path:
                output.add(path)

    except subprocess.CalledProcessError:
        pass
    except FileNotFoundError:   # pragma: no cover
        log.warning('Unable to find `git` in PATH, and therefore, unable to get tracked files.')

    return output


def get_changed_but_unstaged_files() -> Set[str]:
    try:
        files = subprocess.check_output('git diff --name-only'.split()).decode().splitlines()
    except subprocess.CalledProcessError:   # pragma: no cover
        # Since we don't pipe stderr, we get free logging through git.
        raise ValueError

    return set(files)
