""" fit
"""
import click
import hashlib
import imageio
import json
from . import models
import os
import shutil
from sqlalchemy import create_engine, desc, func
import sys
from typing import List, Optional


def exclude(name: str) -> bool:
    """ Checks if file or directory with `name` should be excluded from
        `os.walk`.
    """
    return name.startswith('.')


def find_path_up(filename: str, start: str = '.') -> Optional[str]:
    """ Searchs for `filename` in `start` and all its parent directories until
        `filename` is found or top level is reached.
    """
    start = os.path.abspath(start)
    for dir_part in [os.path.sep.join(start.split(os.path.sep)[:i+1])
                     for i in reversed(
                         range(len(start.split(os.path.sep)))
                     )]:
        if not dir_part:
            dir_part = '/'
        if filename in os.listdir(dir_part):
            return os.path.join(dir_part, filename)


def format_filename(obj, filename: str) -> str:
    """ Formats path for display by making it relative to the repo dir.
    """
    rel_path = os.path.relpath(filename, obj['fit_repo_path'])
    return click.format_filename(rel_path)


def get_keywords(file_path: str) -> List[str]:
    """ Gets XP keywords from file contents.
    """
    try:
        with open(file_path, 'rb') as f:
            image = Image(f.read())
        return image.get('xp_keywords', '').split(';')
    except:
        return []


def hash_file(file_path: str) -> str:
    """ Gets SHA-1 hash of file contents (or pixels if file is an image).
    """
    # Attempt to load image
    try:
        file_bytes = imageio.imread(file_path)
        if not file_bytes.flags.c_contiguous:
            file_bytes = file_bytes.copy(order='C')
    # Load raw bytes of file
    except:
        with open(file_path, 'rb') as f:
            file_bytes = f.read()
    return hashlib.sha1(file_bytes).hexdigest()


def in_repo(obj) -> bool:
    """ Check if current context is within a fit repository.
    """
    if obj['in_repo']:
        return True
    click.echo('fatal: not a fit repository')
    return False


def is_orphan(file_path: str) -> bool:
    """ Checks if number of inode references is one.
    """
    return os.stat(file_path).st_nlink < 2


def process_file(obj, file_path: str, soft=False):
    """ Tracks file in fit repo.
    """
    file_ext = os.path.splitext(file_path)[1]

    # If file is not hard link
    file_query = models.session.query(models.File).filter_by(file=file_path)
    if not file_query.count():
        hash = hash_file(file_path)

        # Append filename to filenames list
        file = models.File.add(hash=hash, file=file_path)

        # Create object if necessary and remove file
        object = os.path.join(obj['fit_path'], 'objects', hash)
        if os.path.exists(object):
            os.remove(file_path)
        else:
            click.echo(f'{hash} CREATE from {format_filename(obj, file_path)!r}')
            os.rename(file_path, object)

        if pack:
            file.packed = True
            models.session.commit()
        else:
            # Create links
            click.echo(f'{hash} LINK ({"soft" if soft else "hard"}) {format_filename(obj, file_path)!r}')
            if soft:
                os.symlink(object, file_path)
            else:
                os.link(object, file_path)


def remove_empty_directories(path: str, clean=False, force=False):
    """ Removes all empty directories in a given path.
    """
    for file in os.listdir(obj['fit_repo_path']):
        if os.path.isdir(file) and not exclude(file):
            for root, dirs, files in os.walk(file, topdown=False):
                if clean:
                    for file in files:
                        file_path = os.path.join(root, file)
                        click.echo(f'Found untracked file: {format_filename(obj, file_path)!r}')
                        if force or click.confirm('Remove?'):
                            click.echo(f'{format_filename(obj, file_path)!r} REMOVE')
                            os.remove(file_path)
                if not os.listdir(root):
                    file_path = os.path.join(obj['fit_repo_path'], root)
                    click.echo(f'{format_filename(obj, file_path)!r} REMOVE (empty directory)')
                    os.rmdir(file_path)
