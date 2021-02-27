# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['confu', 'confu.schema']

package_data = \
{'': ['*']}

install_requires = \
['markdown-include>=0.5,<1']

extras_require = \
{':extra == "docs"': ['mkdocs>=1.0.0,<2.0.0', 'pymdgen<2']}

setup_kwargs = {
    'name': 'confu',
    'version': '1.7.0',
    'description': 'Configuration file validation and generation',
    'long_description': None,
    'author': '20C',
    'author_email': 'code@20c.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/20c/confu',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
