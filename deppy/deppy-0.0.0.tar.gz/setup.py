# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['deppy']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'deppy',
    'version': '0.0.0',
    'description': 'Dependency injection framework for Python',
    'long_description': '# deppy\n\nDependency injection framework for Python\n',
    'author': 'pilagod',
    'author_email': 'pilagooood@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/pilagod/deppy',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
