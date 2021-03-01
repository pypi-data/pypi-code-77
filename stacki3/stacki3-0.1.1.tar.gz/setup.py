# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['stacki3']

package_data = \
{'': ['*']}

install_requires = \
['i3ipc>=2.2.1,<3.0.0']

entry_points = \
{'console_scripts': ['stacki3 = stacki3:main']}

setup_kwargs = {
    'name': 'stacki3',
    'version': '0.1.1',
    'description': 'Stack layout for i3/sway wm.',
    'long_description': '# stacki3\n\nStack layout for i3/sway wm.\n',
    'author': 'Viliam Valent',
    'author_email': 'stacki3@viliamvalent.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ViliamV/stacki3',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
