# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['date_formatter']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'date-formatter',
    'version': '0.1.1',
    'description': 'A Python package for formatting strings into readable date strings',
    'long_description': '# date_time_format\n\na Python package that formats a ten character string to a date\n\n# Installation\n\n```bash\npip install date_formatter\n```\n\n# Usage\n\n## Minimal example\n\n```python\nfrom date_formatter import *\n\ndate_time_string_US = "12-18-2014"\ndate_time_string_AUS = "18-12-2014"\n\nmyDates_US = DateFormatter.dateFormat(date_time_string_US, False, True, "US")\nmyDates_AUS = DateFormatter.dateFormat(date_time_string_AUS, True, False)\n\nprint(myDates_US)\nprint(myDates_AUS)\n\n```\n\n## returns:\n\n- 18-Dec-14\n- 18 December 2014\n\n## Parameters\n\n- **date_time_string: str**\n  The date string you want to format\n- **USE_FULL_MONTH_NAME : bool**\n  Whether to display the full name of the month. If this is set to `True`, shows "January"; if this is set to `False`, shows "Jan".\n- **USE_HYPHEN_AS_SPACER : bool**\n  Whether to show interval between characters as single space, or hyphen. If this is set to `True`, shows "18-Jan-14"; if this set to `False`, shows "18 Jan 14"\n- **REGION_FORMAT : str, optional**\n  Which region\'s date format to use. If set to "US" assumes string is "MM-DD-YYYY"; if this is set to something or is missing, assumes string is "DD-MM-YYYY"\n',
    'author': 'pauladjata',
    'author_email': 'info@adjata.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/pauladjata/date_formatter.git',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
