# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['workreport', 'workreport.tests']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.0,<8.0', 'minilog>=2.0,<3.0']

entry_points = \
{'console_scripts': ['workreport = workreport.cli:main']}

setup_kwargs = {
    'name': 'workreport',
    'version': '0.0',
    'description': 'workreport',
    'long_description': '# Overview\n\nworkreport\n\nThis project was generated with [cookiecutter](https://github.com/audreyr/cookiecutter) using [jacebrowning/template-python](https://github.com/jacebrowning/template-python).\n\n[![Unix Build Status](https://img.shields.io/travis/com/mara/mara.svg?label=unix)](https://travis-ci.com/mara/mara)\n[![Windows Build Status](https://img.shields.io/appveyor/ci/mara/mara.svg?label=windows)](https://ci.appveyor.com/project/mara/mara)\n[![Coverage Status](https://img.shields.io/coveralls/mara/mara.svg)](https://coveralls.io/r/mara/mara)\n[![Scrutinizer Code Quality](https://img.shields.io/scrutinizer/g/mara/mara.svg)](https://scrutinizer-ci.com/g/mara/mara)\n[![PyPI Version](https://img.shields.io/pypi/v/workreport.svg)](https://pypi.org/project/workreport)\n[![PyPI License](https://img.shields.io/pypi/l/workreport.svg)](https://pypi.org/project/workreport)\n\n# Setup\n\n## Requirements\n\n* Python 3.9+\n\n## Installation\n\nInstall it directly into an activated virtual environment:\n\n```text\n$ pip install workreport\n```\n\nor add it to your [Poetry](https://poetry.eustace.io/) project:\n\n```text\n$ poetry add workreport\n```\n\n# Usage\n\nAfter installation, the package can imported:\n\n```text\n$ python\n>>> import workreport\n>>> workreport.__version__\n```\n',
    'author': 'Mara',
    'author_email': 'ma@r.a',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://pypi.org/project/workreport',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
