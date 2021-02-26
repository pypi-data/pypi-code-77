# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['graiax_sayamod_nbnhhsh']

package_data = \
{'': ['*']}

install_requires = \
['aiosonic>=0.9.5,<0.10.0',
 'graia-application-mirai>=0.16.1,<0.17.0',
 'graia-saya>=0.0.4,<0.0.5']

setup_kwargs = {
    'name': 'graiax-sayamod-nbnhhsh',
    'version': '0.1.4',
    'description': '[Saya模块]能不能好好说话——缩写查询',
    'long_description': None,
    'author': 'Eric',
    'author_email': 'erictianc@outlook.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
