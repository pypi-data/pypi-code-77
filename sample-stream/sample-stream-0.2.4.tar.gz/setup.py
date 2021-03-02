# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sample_stream']

package_data = \
{'': ['*']}

extras_require = \
{':python_version < "3.8"': ['importlib_metadata>=3.7.0,<4.0.0']}

entry_points = \
{'console_scripts': ['sample = sample_stream.__main__:main']}

setup_kwargs = {
    'name': 'sample-stream',
    'version': '0.2.4',
    'description': 'Filter lines from standard input according to some probability, with a given delay, and for a certain duration.',
    'long_description': '# sample-stream\n\n<div align="center">\n\n[![Build status](https://github.com/jeroenjanssens/sample-stream/workflows/build/badge.svg?branch=master&event=push)](https://github.com/jeroenjanssens/sample-stream/actions?query=workflow%3Abuild)\n[![Python Version](https://img.shields.io/pypi/pyversions/sample-stream.svg)](https://pypi.org/project/sample-stream/)\n[![Dependencies Status](https://img.shields.io/badge/dependencies-up%20to%20date-brightgreen.svg)](https://github.com/jeroenjanssens/sample-stream/pulls?utf8=%E2%9C%93&q=is%3Apr%20author%3Aapp%2Fdependabot)\n\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![Security: bandit](https://img.shields.io/badge/security-bandit-green.svg)](https://github.com/PyCQA/bandit)\n[![Pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/jeroenjanssens/sample-stream/blob/master/.pre-commit-config.yaml)\n[![Semantic Versions](https://img.shields.io/badge/%F0%9F%9A%80-semantic%20versions-informational.svg)](https://github.com/jeroenjanssens/sample-stream/releases)\n[![License](https://img.shields.io/github/license/jeroenjanssens/sample-stream)](https://github.com/jeroenjanssens/sample-stream/blob/master/LICENSE)\n\n</div>\n\n`sample` is a Python package that allows you to filter lines from standard input according to some probability, with a given delay, and for a certain duration.\n\n\n## Installation\n\nYou can install `sample-stream` as follows:\n\n```console\n$ python -m pip install sample-stream\n```\n\nThis will install an executable `sample` in `~/.local/bin`. You probably want to either add this directory to your `PATH` or create an alias to this executable in a directory which already is on your `PATH`.\n\n\n## Example\n\nThe following command samples lines with a probability of 0.01, with a delay of 1000 milliseconds in between lines, for 5 seconds.\n\n```console\n$ time seq -f "Line %g" 1000000 | sample -r 1% -d 1000 -s 5\nLine 71\nLine 250\nLine 305\nLine 333\nLine 405\nLine 427\nseq -f "Line %g" 1000000  0.01s user 0.00s system 0% cpu 5.092 total\nsample -r 1% -d 1000 -s 5  0.06s user 0.02s system 1% cpu 5.091 total\n```\n\n\n## Help\n\n```console\n$ sample --help\nusage: sample-stream [-h] [-W WEEKS] [-D DAYS] [-H HOURS] [-m MINUTES]\n                     [-s SECONDS] [-t MILLISECONDS] [-u MICROSECONDS]\n                     [-r RATE] [-d DELAY]\n                     [FILE]\n\nFilter lines from standard input according to some probability, with a\ngiven delay, and for a certain duration.\n\npositional arguments:\n  FILE                  File\n\noptional arguments:\n  -h, --help            show this help message and exit\n  -W WEEKS, --weeks WEEKS\n                        Duration of sampling in weeks\n  -D DAYS, --days DAYS  Duration of sampling in days\n  -H HOURS, --hours HOURS\n                        Duration of sampling in hours\n  -m MINUTES, --minutes MINUTES\n                        Duration of sampling in minutes\n  -s SECONDS, --seconds SECONDS\n                        Duration of sampling in seconds\n  -t MILLISECONDS, --milliseconds MILLISECONDS\n                        Duration of sampling in milliseconds\n  -u MICROSECONDS, --microseconds MICROSECONDS\n                        Duration of sampling in microseconds\n  -r RATE, --rate RATE  Rate between 0 and 1 using either 0.33, 33%,\n                        1/3 notation.\n  -d DELAY, --delay DELAY\n                        Time in milliseconds between each line of\n                        output\n```\n\n\n## License\n\n[![License](https://img.shields.io/github/license/jeroenjanssens/sample-stream)](https://github.com/jeroenjanssens/sample-stream/blob/master/LICENSE)\n\nThis project is licensed under the terms of the `MIT` license. See [LICENSE](https://github.com/jeroenjanssens/sample-stream/blob/master/LICENSE) for more details.\n\n\n## Citation\n\n```\n@software{sample-stream,\n  author = {Jeroen H.M. Janssens},\n  title = {{sample-stream} -- Sample lines from a stream},\n  year = {2021},\n  url = {https://github.com/jeroenjanssens/sample-stream},\n  version = {0.2.4}\n}\n```\n\n\n## Credits\n\nThis project was generated with [`python-package-template`](https://github.com/TezRomacH/python-package-template).\n',
    'author': 'Jeroen Janssens',
    'author_email': 'jeroen@jeroenjanssens.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jeroenjanssens/sample-stream',
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
