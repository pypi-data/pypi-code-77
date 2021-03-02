# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bobolink']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0', 'requests>=2.25.1,<3.0.0', 'termcolor>=1.1.0,<2.0.0']

entry_points = \
{'console_scripts': ['bobolink = bobolink.main:cli']}

setup_kwargs = {
    'name': 'bobolink',
    'version': '0.1.0',
    'description': 'bobolink stores bookmarks and helps you search for them later',
    'long_description': '# bobolink-cli\n\nbobolink is a small tool that helps user\'s store bookmarks and search for them later.\nMore specifically, bobolink provides full text search on the HTML documents of the bookmarks that you\'ve saved. In practice, this allows you to use bobolink to save some links, and later search/return all your links which contain for example `"(songbird OR blackbird) AND NOT currawong".`\n\nFor more information on bobolink in general, please refer to the [website](https://bobolink.me)\n\nbobolink-cli is the command line interface to the public instance \nof the bobolink [backend.](https://github.com/jtanza/bobolink/)\n\n### Installation\n\n```\n$ python -m pip install bobolink\n```\n\n### Getting Started\n\nFor user\'s without a bobolink account, the fastest way to get going is to run\n`bobolink signup` after installation. This, followed by `bobolink configure` is all that is needed in order to start saving and searching your bookmarks.\n\nThe cli is heavily documented and can be accessed at anytime directly via \n`bobolink [COMMAND] --help`. Please refer to the terminal session below for an exploration\nof what\'s possible with bobolink.\n',
    'author': 'jtanza',
    'author_email': 'tanzajohn@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jtanza/bobolink-cli',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
