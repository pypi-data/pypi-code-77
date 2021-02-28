# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['elmax', 'elmax.package_one', 'elmax.package_two']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.17,<0.18', 'yarl>=1.6,<2.0']

entry_points = \
{'console_scripts': ['poetry-template = elmax.cli:run']}

setup_kwargs = {
    'name': 'elmax',
    'version': '0.1.1',
    'description': 'Python client for the Elmax CLoud',
    'long_description': '# Python Elmax Cloud client\n\nAsynchronous Python API client for interacting with the Elmax Cloud services.\n\nThis module is not official, developed, supported or endorsed by Elmax.\nFor questions and other inquiries, use the issue tracker in this repo please.\n\n## Installation\n\nThe package is available in the [Python Package Index](https://pypi.python.org/).\n\n```bash\n$ pip3 install elmax --user\n```\n\n## Usage\n\nFor details about the usage please check the `examples.py` file.\n\n## License\n\nThis project is licensed under ASL 2, for more details check LICENSE.\n',
    'author': 'Fabian Affolter',
    'author_email': 'fabian@affolter-engineering.ch',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/home-assistant-ecosystem/python-elmax',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7.0,<4.0.0',
}


setup(**setup_kwargs)
