import os
import sys

from dotenv import load_dotenv


def git_sha():
    """ Gets the git revision, if it exists in cwd """
    cwd = os.getcwd()

    try:
        from .utils.__sha__ import __sha__
    except ImportError as e1:
        import subprocess

        # TODO: import VERBOSITY from utils, print on >1 ?
        # print(repr(e1))
        cwd = os.path.dirname(os.path.abspath(__file__))

        try:
            __sha__ = (
                subprocess.check_output(
                    ["git", "rev-parse", "--short", "HEAD"], cwd=cwd
                )
                .decode()
                .rstrip()
            )
        except FileNotFoundError as e2:
            # print(repr(e2))
            __sha__ = None

    return __sha__


# Check Python version
PY_MIN_VER = (3, 6, 5)
PY_MIN_STR = ".".join(str(x) for x in PY_MIN_VER)
if sys.version_info < PY_MIN_VER:
    ver = ".".join([str(x) for x in sys.version_info[0:3]])
    print("ERROR: nutra requires Python %s or later to run" % PY_MIN_STR)
    print("HINT:  You're running Python " + ver)
    exit(1)

# Read in .env file if it exists locally, else look to env vars
load_dotenv(verbose=False)

NUTRA_DIR = os.path.join(os.path.expanduser("~"), ".nutra")

# Set DB versions here
__db_target_usda__ = "0.0.7"
__db_target_nt__ = "0.0.0"


# Package info
__title__ = "nutra"
__version__ = "0.2.0.dev5"
__sha__ = git_sha()
__author__ = "Shane Jaroch"
__license__ = "GPL v3"
__copyright__ = "Copyright 2018-2020 Shane Jaroch"
