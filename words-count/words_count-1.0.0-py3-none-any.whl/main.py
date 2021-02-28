#!/usr/bin/env python

from words_count.parser import WordsCount
import argparse
import json
import fileinput
import sys

parser = argparse.ArgumentParser(
    description="""
    CLI tool for that outputs the N (N by default 100) most common n-word (n by default is 3) sequence in text,
    along with a count of how many times each occurred in the text.
    """
)
parser.add_argument('-f', '--files', nargs='*', help='Files path to read', required=False, default=[])
parser.add_argument('-n', '--number-of-words', help='Number of words to group', required=False, type=int, default=3)
parser.add_argument('-t', '--top', help='Max number of groups of words to output', required=False, type=int, default=100)
args = parser.parse_args()


def main():
    if not sys.stdin.isatty() and args.files:
        sys.exit(
            "You should use 'stdin' OR positional arguments (--file, --number-of-words, --top) as input," "but not both"
        )

    words_counter = WordsCount(chunk_size=args.number_of_words, top_number=args.top)

    if not sys.stdin.isatty():
        for line in fileinput.input():
            words_counter.count(line=line)
    else:
        words_counter.count_in_files(files_path=args.files)

    print(json.dumps(words_counter.result, sort_keys=False, indent=4))


if __name__ == "__main__":
    main()
