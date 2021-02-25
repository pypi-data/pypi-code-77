# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['twacapic']

package_data = \
{'': ['*']}

install_requires = \
['TwitterAPI>=2.6.9,<3.0.0']

setup_kwargs = {
    'name': 'twacapic',
    'version': '0.1.1',
    'description': 'A Twitter Academic API Client',
    'long_description': '# twacapic\nTwitter Academic API Client\n',
    'author': 'Felix Victor Münch',
    'author_email': 'f.muench@leibniz-hbi.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Leibniz-HBI/twacapic',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
