# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tktabl']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'tktabl',
    'version': '0.2.0',
    'description': 'Python Tkinter Table complement',
    'long_description': '# tktabl\n\nThis proyect intends to be a complement on managing tables within the Python Tkinter GUI.\n\n## Installation\n\nRun the following to install:\n\n```shell\n$ pip install tktabl\n```\n\n## Usage\n\n### Import\n\nAs tktable is a complement to tkinter, you must import it in your code:\n\n```python\nimport tkinter as tk\nimport tktabl\n```\n\n### Create a table\n\nCreating a table requires a tkinter root as an argument. This will create a\ndefault 5x4 table in its own tkinter frame.\nNote that the first row is a column headers row.\n\n```python\nroot = tk.Tk()\ntable = tktable.Table(root)\ntable.pack()\n```\n\nYou can specify it size passing 2 additional arguments (col, row), e.g.:\n\n```python\nroot = tk.Tk()\ntable = tktable.Table(root, col=3, row=5)\ntable.pack()\n```\n\nThis will create a 6x3 table where the first row is a column headers row.\n\nYou can pass a list of strings as column headers, e.g.:\n\n```python\n\nheaders = ["ID", "Name", "Age"]\n\nroot = tk.Tk()\ntable = tktable.Table(root, headers=headers)\ntable.pack()\n```\n\nThis will create a 5x3 table where the first row is the column headers row\nwith the values "ID", "Name", and "Age" respectively\n\nYou can pass a list of dictionaries with the data you want to display, e.g.:\n\n```python\n\ndata = [\n    {"ID": 1, "Name": "Juan", "Age": 24},\n    {"ID": 2, "Address": "5th 20-22"}\n]\n\nroot = tk.Tk()\ntable = tktable.Table(root, data=data)\ntable.pack()\n```\n\nNote that not every dictionary has the same keys.\nThis, will create a 4x3 table.\nFirst row will be a row with headers "ID", "Name", "Age" and "Address".\nSecond row will be the data of the first dictionary.\nThird row will be the data of the second dictionary.\n(If the dictionary doesn\'t has any value in a given header, the corresponding\ncell will be left blank)\n\nFinally, you can mix all these arguments, e.g.:\n\n```python\n...\ntable = tktable.Table(root, row=5, headers=headers, data=data)\ntable.pack()\n```\n\nIn this case, it will create a table where there will be as many columns\nas headers in the headers variable plus the data variable without repeating themselves\n\nAfter creating the table and before running your app, you must pack it with the Table.pack() function.\n\n### Usefull methods\n\n- Table.get_cell(row, column): will return a Cell object in the corresponding\n  row and column.\n\n- Table.get_data(): will return a list of dictionaries, as many as rows are in the table, ignoring\n  headers row, and each dictionary will have as many named keys as columns are in the table.\n\n- Table.get_row_data(row): will return a dictionary with as many keys as columns are in the table and\n  with values corresponding the number of row passed as argument (Row 0 is the first row **after** the\n  header row)\n\n- Cell.get_value(): will return the value displayed by the cell\n\n- Cell.set_value(value): Cell will display the value passed as argument\n\n### Some features\n\nSimple left click on a cell will highlight it.\nDouble left click will highlight its row.\nTriple left click will highlight its column.\n\nWork in progress...\n\n## Changelog\n\nv 0.2.0[02/28/2021]: The table includes its own tkinter frame master. Added set and get data functions.\n',
    'author': 'Juan José Abuin',
    'author_email': 'juanj.abuin@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/DaShagy/python-tktable',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
