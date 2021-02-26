import sys
import re
import os
from argparse import ArgumentParser
from termcolor import colored
import itertools as it

from lookfor.__init__ import __version__


def find_fd(file_dir):
    '''search recursively for a file or directory from cwd'''
    count = 0
    regex = re.compile(file_dir)
    for root, dirs, files in os.walk('.'):
        for (a, b) in it.zip_longest(dirs, files):
            if a:
                if regex.search(a):
                    print(os.path.join(root, colored(a, 'red', attrs=['bold'])))
                    count += 1
            if b:
                if regex.search(b):
                    print(os.path.join(root, colored(b, 'red', attrs=['bold'])))
                    count += 1
    # for testing purposes
    if count == 0:
        return 0
    if count > 0:
        return 1


def find_ext(ext):
    '''search recursively for ext from cwd'''
    count = 0 #keep track of number of found files

    # prevent this function from being just a file search
    if ext.find('.') != -1:
        if ext[0] != '.':
            return 0

    for root, dirs, files in os.walk('.'):
        for name in files:
            if name.endswith(ext):
                # if found, print path to file
                print(os.path.join(root, colored(name, 'red', attrs=['bold'])))
                count += 1
    print('found {} {} files'.format(count, colored(ext, 'red', attrs=['bold'])))
    # for testing purposes
    if count == 0:
        return 0
    if count > 0:
        return 1


def print_usage():
    print('Usage: lookfor <command> <arg>')
    print('\t--file, -f:\tsearch for a file/directory recursively')
    print('\t--ext, -e:\tsearch for files of extension recursively')
    print('\t--version, -V:\tshow version info')
    print('\t--usage, -u:\tshow usage and quit')



def main():
    argp = ArgumentParser(description='Look for things...')
    argp.add_argument('--file', '-f', help='search for a file/directory recursively')
    argp.add_argument('--ext', '-e', help='search for files of ext recursively')
    argp.add_argument('--usage', '-u', action='store_true', help='show usage and quit')
    argp.add_argument('--version', '-V', action='store_true', help='show version info')


    results = argp.parse_args()
    
    if results.file:
        find_fd(results.file)
    elif results.ext:
        find_ext(results.ext)
    elif results.usage:
        print_usage()
    elif results.version:
        print(f'lookfor {__version__}')
    else:
        print_usage()
        sys.exit(1)
    
if __name__ == '__main__' :
    main()