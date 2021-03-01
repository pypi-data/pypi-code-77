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
    'version': '0.2.1',
    'description': 'Stack layout for i3/sway wm.',
    'long_description': '# stacki3\n\nSimple stack layout for i3/sway wm.\n\n## Instalation\n\n1. Install the package\n\n```bash\npip install --user stacki3\n```\n\n2. Inside your i3/sway config add\n\n```i3\nexec_always stacki3 45\n```\n\n3. Restart i3/sway\n',
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
