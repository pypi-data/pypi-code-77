# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['simple_note_taker']

package_data = \
{'': ['*']}

install_requires = \
['colorama>=0.4.4,<0.5.0', 'typer>=0.3.2,<0.4.0']

entry_points = \
{'console_scripts': ['snt = simple_note_taker.main:app']}

setup_kwargs = {
    'name': 'simple-note-taker',
    'version': '0.1.0',
    'description': '',
    'long_description': '',
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
