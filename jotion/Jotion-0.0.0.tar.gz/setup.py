# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jotion']

package_data = \
{'': ['*']}

install_requires = \
['atlassian-python-api>=3.5.3,<4.0.0',
 'jira-cli>=3.0,<4.0',
 'jira>=2.0.0,<3.0.0',
 'notion>=0.0.28,<0.0.29']

setup_kwargs = {
    'name': 'jotion',
    'version': '0.0.0',
    'description': '2-way, live Notion<>Jira integration.',
    'long_description': None,
    'author': 'Gilad Barnea',
    'author_email': 'cr-gbarn-herolo@allot.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
