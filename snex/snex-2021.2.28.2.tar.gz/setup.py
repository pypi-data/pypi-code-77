# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['snex', 'snex.cli']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0', 'pyhocon>=0.3.57,<0.4.0', 'pystache>=0.5.4,<0.6.0']

entry_points = \
{'console_scripts': ['snex = snex.cli:main']}

setup_kwargs = {
    'name': 'snex',
    'version': '2021.2.28.2',
    'description': 'snex - snippet extractor',
    'long_description': 'snex - snippet extractor\n========================\n\nExtract snippets for blog posts or examples.\n\nHow to use\n\nInstallation\n------------\n\n::\n\n   pip install snex\n\nSetup\n-----\n\ncreate a snex.conf in the root directory of a project you want to create\nsnippets from:\n\n::\n\n   config {\n     default {\n       output_path: "snippets"\n       comment_prefix: "# "\n       comment_suffix: ""\n     }\n\n     src {\n       lang: "python"\n       root: "src"\n       glob: "**/*.py"\n     }\n   }\n\nThe config syntax is\n`HOCON <https://github.com/typesafehub/config/blob/master/HOCON.md>`__,\nunder the hood `pyhocon <https://github.com/chimpler/pyhocon>`__.\n\nYou have 3 layers of settings in a section:\n\n1. the global default config\n   ```docs/snippets/global-default-config.md`` <docs/snippets/global-default-config.md>`__.\n2. the config section ``default`` in your ``snex.conf`` file (which\n   overwrites the global default).\n3. the specific config section in your ``snex.conf`` (the section name\n   is only for the show, it does not have any effect. Only ``default``\n   is reserved.). The configuration in a specific section overwrites the\n   default section which overwrites the global default config.\n\nRun\n---\n\nLet’s assume that you have a project in ``/path/to/your/project``. You\ncreated a ``/path/to/your/project/snex.conf`` like described in the\nprevious topic.\n\nFrom the project directory\n~~~~~~~~~~~~~~~~~~~~~~~~~~\n\n::\n\n   cd /path/to/your/project\n   snex\n\nThis will read ``snex.conf`` in the current directory and dump the\nsnippets into the configured ``output_path``.\n\nFrom a different directory\n~~~~~~~~~~~~~~~~~~~~~~~~~~\n\n::\n\n   snex /path/to/your/project\n\nThis will read ``/path/to/your/project/snex.conf`` and dump the snippets\ninto the configured ``output_path``.\n\nFrom a different directory to a different snippet output directory\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n\n::\n\n   snex /path/to/your/project /path/custom/snippet/output/dir\n\nThis will read ``/path/to/your/project/snex.conf`` and dump the snippets\ninto ``/path/custom/snippet/output/dir``.\n\n**TAKE CARE**\n\nThis invocation will overwrite the output dir of all defined config\nsections. Which means that all snippets are dumped into the same\ndirectory.\n',
    'author': 'Joachim Bargsten',
    'author_email': 'jw@bargsten.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jwbargsten/snex',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
