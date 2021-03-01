# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['librelingo_yaml_loader']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0',
 'librelingo-types>=0.1.0,<0.2.0',
 'pyfakefs>=4.3.3,<5.0.0',
 'python-slugify>=4.0.1,<5.0.0',
 'pyyaml>=5.3.1,<6.0.0',
 'slugify>=0.0.1,<0.0.2',
 'snapshottest>=0.6.0,<0.7.0']

setup_kwargs = {
    'name': 'librelingo-yaml-loader',
    'version': '0.1.3',
    'description': 'Load YAML-based LibreLingo courses in your Python project.',
    'long_description': '# librelingo-yaml-loader\n\nlibrelingo-yaml-loader can be used to load YAML-based LibreLingo courses in Python programs.\n\nThe course is loaded into the types from `[libreling-types](https://pypi.org/project/librelingo-types/).\n\n## Usage\n\n```python\nfrom librelingo_yaml_loader import yaml_loader\n\ncourse = yaml_loader.load_course("./path/to/my/course")\n```\n\n`load_course` returns a [Course()](https://github.com/kantord/LibreLingo/blob/main/apps/librelingo_yaml_loader/librelingo_yaml_loader/data_types.py) object\n\n',
    'author': 'Dániel Kántor',
    'author_email': 'git@daniel-kantor.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
