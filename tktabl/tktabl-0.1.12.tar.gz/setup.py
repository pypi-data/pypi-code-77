# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tktabl']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'tktabl',
    'version': '0.1.12',
    'description': 'Python Tkinter Table complement',
    'long_description': '# tktabl\n\nThis proyect intends to be a complement on managing tables within the Python Tkinter GUI.\n\n## Installation\n\nRun the following to install:\n\n```shell\n$ pip install tktabl\n```\n\n## Usage\n\nAs tktable is a complement to tkinter, you must import it in your code:\n\n```python\nimport tkinter as tk\nimport tktabl\n```\n\nA table needs a tkinter Frame as its master\n\n```python\nroot = tk.Tk()\nframe = tk.Frame(root)\ntable = tktable.Table(frame)\nframe.pack()\n```\n\nBy default, it creates a 4x4 table in the specified frame.\nYou can also specify it size passing 2 additional arguments (col, row), e.g.\n\n```python\nroot = tk.Tk()\nframe = tk.Frame(root)\ntable = tktable.Table(frame, col=3, row=5)\nframe.pack()\n```\n\nBefore you pack the frame, you can also set each cell value. To do that, you can access each cell\nwith the \'get_cell()\' method, passing it position (row, column) within the table. e.g.\n\n```python\nroot = tk.Tk()\nframe = tk.Frame(root)\ntable = tktable.Table(frame, col=3, row=5)\nmy_cell = table.get_cell(2,2)\nframe.pack()\n```\n\nNow, the my_cell variable is associated with the cell in the _third_ row and the _third_ column\n\nYou can set the value it displays with the Cell set_value(_"value"_) method.\n\n```python\n...\ntable = tktable.Table(frame, col=3, row=5)\nmy_cell = table.get_cell(2,2)\nmy_cell.set_value("Hello World!")\nframe.pack()\n```\n\nNow the cell will display the string "Hellow World!"\n\nYou can also get its value with the Cell get_value() method.\n\nSimple left click on a cell will highlight it.\nDouble left click will highlight its row.\nTriple left click will highlight its column.\n\nWork in progress...\n',
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
