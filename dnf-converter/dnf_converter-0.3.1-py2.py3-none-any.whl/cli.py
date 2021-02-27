"""
Module that contains the command line app.

Why does this file exist, and why not put this in __main__?

  You might be tempted to import things from __main__ later, but that will cause
  problems: the code will get executed twice:

  - When you run `python -mdnf_converter` python will execute
    ``__main__.py`` as a script. That means there won't be any
    ``dnf_converter.__main__`` in ``sys.modules``.
  - When you import __main__ it will get executed again (as a module) because
    there's no ``dnf_converter.__main__`` in ``sys.modules``.

  Also see (1) from http://click.pocoo.org/5/setuptools/#setuptools-integration
"""
import sys
import argparse
import dnf_converter as dnf
import argparse
from dnf_converter.flask_app import start_flask
from dnf_converter.dnf_converter import get_dnfs

def main(argv=sys.argv):
  parser=argparse.ArgumentParser()
  parser.add_argument('--web', help='Start a Webserver', nargs='?', const=1, type=int)
  parser.add_argument('--cli', help='Do not start a Webserver', nargs='+')
  args=parser.parse_args()
  if args.web is not None:
    start_flask()
    return 0
  elif args.cli is not None:
    result = get_dnfs(args.cli)
    return result
  else:
    print(args)
    return 0
  

if __name__ == '__main__':
  main()