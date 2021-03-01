# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['roam_to_git']

package_data = \
{'': ['*']}

install_requires = \
['GitPython>=3.1.14,<4.0.0',
 'loguru>=0.5.3,<0.6.0',
 'pathvalidate>=2.3.2,<3.0.0',
 'psutil>=5.8.0,<6.0.0',
 'python-dotenv>=0.15.0,<0.16.0',
 'selenium>=3.141.0,<4.0.0']

extras_require = \
{'test': ['mypy>=0.812,<0.813']}

entry_points = \
{'console_scripts': ['roam-to-git = roam_to_git.__main__:main']}

setup_kwargs = {
    'name': 'roam-to-git',
    'version': '0.2.1',
    'description': 'Automatic RoamResearch backup to Git',
    'long_description': None,
    'author': 'Matthieu Bizien',
    'author_email': 'matthieu@yokai.ai',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/MatthieuBizien/roam-to-git',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
