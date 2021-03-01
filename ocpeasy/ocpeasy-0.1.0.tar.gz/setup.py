# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ocpeasy']

package_data = \
{'': ['*']}

install_requires = \
['GitPython>=3.1.12,<4.0.0',
 'PyYAML>=5.3.1,<6.0.0',
 'cryptography==3.4.5',
 'fire>=0.3.1,<0.4.0',
 'openshift-client==1.0.12',
 'sh>=1.14.1,<2.0.0',
 'simple-term-menu>=0.10.4,<0.11.0']

setup_kwargs = {
    'name': 'ocpeasy',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'David Barrat',
    'author_email': 'david@barrat.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
