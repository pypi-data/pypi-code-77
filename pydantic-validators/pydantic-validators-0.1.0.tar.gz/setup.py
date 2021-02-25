# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pydantic_validators']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pydantic-validators',
    'version': '0.1.0',
    'description': '',
    'long_description': '<h1 align="center">\n    <strong>pydantic-validators</strong>\n</h1>\n<p align="center">\n    <a href="https://github.com/Kludex/pydantic-validators" target="_blank">\n        <img src="https://img.shields.io/github/last-commit/Kludex/pydantic-validators" alt="Latest Commit">\n    </a>\n        <img src="https://img.shields.io/github/workflow/status/Kludex/pydantic-validators/Test">\n        <img src="https://img.shields.io/codecov/c/github/Kludex/pydantic-validators">\n    <br />\n    <a href="https://pypi.org/project/pydantic-validators" target="_blank">\n        <img src="https://img.shields.io/pypi/v/pydantic-validators" alt="Package version">\n    </a>\n    <img src="https://img.shields.io/pypi/pyversions/pydantic-validators">\n    <img src="https://img.shields.io/github/license/Kludex/pydantic-validators">\n</p>\n\n\n## Installation\n\n``` bash\npip install pydantic-validators\n```\n\n## License\n\nThis project is licensed under the terms of the MIT license.\n',
    'author': 'Marcelo Trylesinski',
    'author_email': 'marcelotryle@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Kludex/pydantic-validators',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
