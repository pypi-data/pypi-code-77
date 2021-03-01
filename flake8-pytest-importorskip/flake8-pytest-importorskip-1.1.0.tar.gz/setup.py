# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['flake8_pytest_importorskip']

package_data = \
{'': ['*']}

install_requires = \
['flake8>=3', 'kgb>=6.0,<7.0', 'pycodestyle>=2.6.0,<3.0.0']

entry_points = \
{'flake8.extension': ['PIS = flake8_pytest_importorskip:Plugin']}

setup_kwargs = {
    'name': 'flake8-pytest-importorskip',
    'version': '1.1.0',
    'description': 'Make pycodestyle treat pytest.importorskip as an import statement (avoid E402)',
    'long_description': '# flake8-pytest-importorskip\n\n[![pypi](https://badge.fury.io/py/flake8-pytest-importorskip.svg)](https://pypi.org/project/flake8-pytest-importorskip)\n[![Python: 3.6+](https://img.shields.io/badge/Python-3.6+-blue.svg)](https://pypi.org/project/flake8-pytest-importorskip)\n[![Downloads](https://img.shields.io/pypi/dm/flake8-pytest-importorskip.svg)](https://pypistats.org/packages/flake8-pytest-importorskip)\n![Build Status](https://img.shields.io/github/checks-status/ashb/flake8-pytest-importorskip/main)\n[![Code coverage](https://codecov.io/gh/ashb/flake8-pytest-importorskip/branch/main/graph/badge.svg)](https://codecov.io/gh/ashb/flake8-pytest-importorskip)\n[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-green.svg)](https://en.wikipedia.org/wiki/Apache_License)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)\n\n## Description\n\nTreat `pytest.importorskip` as an import statement, not code, to silence the "module level import not at top of file" (E402) from pycodestyle\n\nIt allows code such as this to pass without having to globally disable E402.\n\nIt does this in a _slightly_ hacky way (see the docs of [kgb] for details) , so it may break in future versions of pycodestyle.\n\n### Checks:\n\nNone\n\n## Installation\n\n    pip install flake8-pytest-importorskip\n\n## Usage\n\n`flake8 <your code>`\n\n## For developers\n\n### Create venv and install deps\n\n    make init\n\n### Install git precommit hook\n\n    make precommit_install\n\n### Run linters, autoformat, tests etc.\n\n    make pretty lint test\n\n### Bump new version\n\n    make bump_major\n    make bump_minor\n    make bump_patch\n\n## License\n\nApache 2.0\n\n[kgb]: https://github.com/beanbaginc/kgb\n\n## Change Log\n\nUnreleased\n-----\n\n* ...\n\n1.1.0 - 2021-03-01\n-----\n\n* Replace accessing private state of flake8 plugins with wrapping/spying on function, using [kgb]\n\n1.0.0 - 2021-02-19\n-----\n\n* initial\n',
    'author': 'Ash Berlin-Taylor',
    'author_email': 'ash@apache.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://pypi.org/project/flake8-pytest-importorskip',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
