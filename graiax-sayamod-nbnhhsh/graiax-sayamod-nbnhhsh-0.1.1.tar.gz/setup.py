# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['graiax_sayamod_nbnhhsh']

package_data = \
{'': ['*']}

install_requires = \
['graia-application-mirai>=0.16.1,<0.17.0',
 'graia-broadcast>=0.7.0,<0.8.0',
 'graia-saya>=0.0.4,<0.0.5',
 'requests>=2.25.1,<3.0.0']

setup_kwargs = {
    'name': 'graiax-sayamod-nbnhhsh',
    'version': '0.1.1',
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
