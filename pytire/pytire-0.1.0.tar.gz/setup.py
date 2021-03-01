# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pytire']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pytire',
    'version': '0.1.0',
    'description': 'Python library to handle tire attributes.',
    'long_description': '# pytire\n[![Documentation Status](https://readthedocs.org/projects/pytire/badge/?version=latest)](https://pytire.readthedocs.io/en/latest/?badge=latest)\n\nA library to make interpreting tire attributes and calculations easier.\n\n### Table of Contents\n## Getting Started\nTo use this library install it via pip\n\n```sh\n$ pip install pytire\n```\n\nimport into python\n```python\nfrom pytire import Tire\n\ntire = Tire("34x10.75-16")\n```\n\n## Dev Setup\n\nClone from github\n```\n$ git clone \n```\n\nInstall using poetry\n```sh\n$ poetry install\n```\nset up pre-commit\n```sh\n$ pre-commit install\n```\n\nAlternatively use the dev container.\n',
    'author': 'girotobial',
    'author_email': 'abrobinson1907@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/girotobial/pytire',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
