import argparse
import os
import sys

from blessed import Terminal
from ruamel.yaml import YAML
from box import Box

from .ui import ui_loop


yaml = YAML(typ="safe")


def _get_args():
    parser = argparse.ArgumentParser(
        description="Show your route notes in a pleasing and terminal-friendly format"
    )
    parser.add_argument("file_name")
    return parser.parse_args()


def main():
    args = _get_args()
    term = Terminal()

    if not os.path.exists(args.file_name):
        print(f"{args.file_name} does not exist")
        return 1

    with open(args.file_name) as f:
        data = yaml.load(f)

    with term.cbreak(), term.fullscreen(), term.hidden_cursor():
        ui_loop(term, Box(data))


if __name__ == "__main__":
    sys.exit(main())
