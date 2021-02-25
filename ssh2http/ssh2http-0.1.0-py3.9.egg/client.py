import sys

import requests

from ssh2http import HelpException

DEFAULT_TIMEOUT = 30


def usage(name=sys.argv[0]):
    return f"""
    {name} <http> <timeout: optional, defaults to 30>
    """


def get_args(default_timeout=DEFAULT_TIMEOUT):
    args = sys.argv

    if len(args) < 2:
        raise HelpException(usage())
    if len(args) == 2:
        args += [default_timeout]

    return args


if __name__ == '__main__':
    host, timeout = get_args()

    while True:
        try:
            command = input(">>> ")
            print(requests.post(host, json=dict(command=command, timeout=timeout)).json()["response"])
            print()
        except KeyboardInterrupt:
            print("Bye")
