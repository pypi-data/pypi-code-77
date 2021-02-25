# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['callpass', 'callpass.validated_callpass']

package_data = \
{'': ['*']}

install_requires = \
['cachecontrol', 'requests']

entry_points = \
{'console_scripts': ['callpass = callpass.__main__:main']}

setup_kwargs = {
    'name': 'callpass',
    'version': '0.4.0',
    'description': 'Generate APRS-IS callpasses',
    'long_description': None,
    'author': 'Kyle Jones',
    'author_email': 'kyle@kf5jwc.us',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/kf5jwc/callpass-py',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
