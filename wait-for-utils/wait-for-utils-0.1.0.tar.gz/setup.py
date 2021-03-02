# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['wait_for_utils']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0', 'psycopg2>=2.8.6,<3.0.0']

entry_points = \
{'console_scripts': ['wait-for-postgres = '
                     'wait_for_utils.cli:wait_for_postgres']}

setup_kwargs = {
    'name': 'wait-for-utils',
    'version': '0.1.0',
    'description': 'Wait for PostgreSQL to be available before startup docker container.',
    'long_description': '# wait-for-utils\n![Python Main Release](https://github.com/mtizima/wait-for-utils/workflows/Python%20Main%20Release/badge.svg)\n\nWait for service(s) to be available before startup docker container.\n\n## Installation\n```bash\npip install wait-for-utils\n```\n\n## Usage\n\n\n#### PostgreSQL\nExample:\n```bash\nwait-for-postgres -\n```\nAdditional documentation:\n```bash\nwait-for-postgres --help\n```\n\nBy default, all settings are taken from the environment variables.\n* **POSTGRES_DB**\n* **POSTGRES_USER**\n* **POSTGRES_PASSWORD**\n* **POSTGRES_HOST**\n* **POSTGRES_PORT** \n* **POSTGRES_CHECK_TIMEOUT**\n* **POSTGRES_CHECK_INTERVAL**\n',
    'author': 'Dmitry',
    'author_email': 'mtizima@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mtizima/wait-for-utils',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
