import argparse
from py_build.main import main
from . import name

parser = argparse.ArgumentParser("python -m " + name.split('/')[1], description='Runs the given build targets in order given')
parser.add_argument('target', nargs='+', help='Target or targets for the build action')
parser.add_argument('-P', '--package', action='store', default='_build', help='Python package where the build modules are found')
args = parser.parse_args()

exit(main(args.package, *args.target))