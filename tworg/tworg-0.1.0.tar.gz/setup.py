# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tworg']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['tworg = tworg.console:run']}

setup_kwargs = {
    'name': 'tworg',
    'version': '0.1.0',
    'description': 'Convert TiddlyWiki tiddler files to Org Mode',
    'long_description': '# tworg\n\nThis is a small program to convert [TiddlyWiki](https://tiddlywiki.com/) tiddler (`*.tid`) files into [Org Mode](https://orgmode.org/) files.\n\nThis is not at all production-ready and was written as a one-off thing to convert my TiddlyWiki into a set of org files. As such, it makes a few assumptions:\n\n- The only metadata it preserves in the org files are `TITLE`, `AUTHOR`, and `TAGS`.\n- It replaces links to other tiddlers with Org-roam links. Thus, it assumes you are using [Org-roam](https://www.orgroam.com/).\n- Definitely not 100% coverage of the TiddlyWiki markup syntax.\n\n## Usage\n\n``` shell\nusage: tworg [-h] [-o OUTPUT] tiddler [tiddler ...]\n\nConvert .tid TiddlyWiki files into Org Mode files.\n\npositional arguments:\n  tiddler               Tiddlers to convert\n\noptional arguments:\n  -h, --help            show this help message and exit\n  -o OUTPUT, --output OUTPUT\n                        Directory to write org files to\n```\n\nExample, converting all TiddlyWiki files in `~/tiddlywiki/` to Org Mode files in `~/org/`:\n\n``` shell\ntworg -o ~/org/ ~/tiddlywiki/*.tid\n```\n\n',
    'author': 'Kyle Johnston',
    'author_email': 'kyle@muumu.us',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/kylerjohnston/tworg',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
