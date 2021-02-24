# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['voicemailbox']

package_data = \
{'': ['*'],
 'voicemailbox': ['static/fonts/*', 'static/images/*', 'static/songs/*']}

install_requires = \
['IMAPClient>=2.2.0,<3.0.0',
 'PyYAML>=5.4.1,<6.0.0',
 'kivy>=2.0.0,<3.0.0',
 'python-dotenv>=0.15.0,<0.16.0',
 'rpi-backlight>=2.2.0,<3.0.0']

setup_kwargs = {
    'name': 'voicemailbox',
    'version': '0.1.0',
    'description': 'Application for reading voice messages',
    'long_description': None,
    'author': 'Pierre Gobin',
    'author_email': 'dev@pierregobin.fr',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
