# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['simple_note_taker']

package_data = \
{'': ['*']}

install_requires = \
['colorama>=0.4.4,<0.5.0',
 'tinydb-serialization>=2.1.0,<3.0.0',
 'tinydb>=4.4.0,<5.0.0',
 'typer>=0.3.2,<0.4.0']

entry_points = \
{'console_scripts': ['snt = simple_note_taker.main:app']}

setup_kwargs = {
    'name': 'simple-note-taker',
    'version': '0.1.2',
    'description': '',
    'long_description': 'A simple CLI note taker, written in Python.\n\nHome: https://github.com/GitToby/simple_note_taker\n\nStart with\n```commandline\npip install simple_note_taker\n```\n\nThen:\n```commandline\nsnt --help\n```\n\nDev with [Poetry](https://python-poetry.org/)',
    'author': 'Toby',
    'author_email': 'toby@thedevlins.biz',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
