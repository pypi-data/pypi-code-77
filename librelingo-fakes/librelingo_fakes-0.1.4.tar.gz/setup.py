# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['librelingo_fakes']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'librelingo-fakes',
    'version': '0.1.4',
    'description': 'Fake data for testing LibreLingo-related packages',
    'long_description': "# librelingo-fakes\n\nThis package contains fake data for testing LibreLingo-related packages.\n\nThe fake data is returned using the types from `[libreling-types](https://pypi.org/project/librelingo-types/).\n\n## Usage\n```python\n\nfrom librelingo_fakes import fakes\n\nfakes.course1  # This is a Course() object\nfakes.course2  # This is another Course() object\nfakes.courseEmpty  # This is an empty course\n```\n\nFor the full list of fakes, use the autocomplete or check out the [this file](https://github.com/kantord/LibreLingo/blob/main/apps/librelingo_fakes/librelingo_fakes/fakes.py).\n\n### Customizing fakes\n\nYou can use `fakes.customize` to change some attributes on a fake object.\nIf you want to change the modules on `fakes.course1`, you'd do it like this:\n\n```python\nfake_course = fakes.customize(fakes.course1, modules=[\n    fake_module_1, fake_module_2\n])\n```\n\n\n",
    'author': 'Dániel Kántor',
    'author_email': 'git@daniel-kantor.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
