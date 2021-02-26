# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['twacapic']

package_data = \
{'': ['*']}

install_requires = \
['TwitterAPI>=2.6.9,<3.0.0']

entry_points = \
{'console_scripts': ['twacapic = twacapic.main:run']}

setup_kwargs = {
    'name': 'twacapic',
    'version': '0.1.3.3',
    'description': 'A Twitter Academic API Client',
    'long_description': '# twacapic\n\nTwitter Academic API Client\n\nIn development. Not even ready for experimental use!\n\n\n## Installation\n\nInstall via pip:\n\n`pip install twacapic`\n\n\n## Dev Install\n\n1. Install [poetry](https://python-poetry.org/docs/#installation)\n2. Clone repository\n3. In the directory run `poetry install`\n4. Run `poetry shell` to start development virtualenv\n\n',
    'author': 'Felix Victor Münch',
    'author_email': 'f.muench@leibniz-hbi.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Leibniz-HBI/twacapic',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
