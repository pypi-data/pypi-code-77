import argparse
import itertools
import random
import threading
import time
from textwrap import shorten, wrap
from typing import Optional

from joke.joke import random, random_10
from spinner import Spinner

def random_joke():
    result = random()
    wrapped_joke = f"""
Question: {result['question']}
Answer: {result['answer']}
Type: {result['type']}
    """
    return wrapped_joke

def color(string: str) -> str:
    string = f"\033[32m{string}\033[0m"
    return string

def cli():
    spinner = Spinner()
    spinner.start()
    joke = random_joke()
    spinner.stop()
    return color(joke)

if __name__ == "__main__":
    cli()