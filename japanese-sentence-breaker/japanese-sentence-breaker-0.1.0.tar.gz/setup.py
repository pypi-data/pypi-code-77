# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['japanese_sentence_breaker']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'japanese-sentence-breaker',
    'version': '0.1.0',
    'description': '',
    'long_description': '# Japanese Sentence Breaker\n\n日本語の文を「。」を基準に改行区切りします。\n\n## Instllation\n\n```bash\npip install japanese-sentence-breaker\n```\n\n\n## Usage\n\n```python\nfrom japanese_sentence_breaker import break_line\n\n\ntext = "これはテストです。文の流れを考慮し、句点区切りで文章を分割します。「例えば。」このようなカッコ内のテキストは分割しません。"\nout = break_line(text)\n\nprint(out)\n# これはテストです。\n# 文の流れを考慮し、句点区切りで文章を分割します。\n# 「例えば。」このようなカッコ内のテキストは分割しません。\n\n\ntext = "これは「テストです。｛整合性の取れないカッコは消去されます。）"\nout = break_line(text)\n\nprint(out)\n# これはテストです。\n# 整合性の取れないカッコは消去されます。\n\n\ntext = "これは「テストです。｛整合性のないカッコは無視されます。）改行はできません。"\nout = break_line(text)\n\nprint(out)\n# これは「テストです。｛整合性のないカッコは無視されます。）改行はできません。\n```',
    'author': 'hppRC',
    'author_email': 'hpp.ricecake@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/hpprc/japanese-sentence-breaker',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
