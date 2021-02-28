# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['commando']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pycommando',
    'version': '0.1.1',
    'description': 'A framework for batch processing.',
    'long_description': '# Commando\n\nCommando is a framework for batch processing.\n\nコマンドラインツールを脳筋で実行していくバッチ処理のためのフレームワーク。\n基本的にPythonの構文でワークフローを構築できるので、バッチ処理での変数の取り回しなどがしやすいのがメリット。\n\nShell Script や Bat ファイルを書かなくても実行したいコマンドさえわかっていればバッチ処理が書ける。\n\n**コンセプト**\n- バッチ処理ワークフローを構築するためのフレームワーク\n- 逐次処理で書く\n- 外部コマンドに関しては subprocess.run()が走る\n\n**Feature**\n- add()でコマンド追加\n- 追加された順に処理する\n- execute() で追加されたコマンドの実行\n- 関数もコマンドとして実行できる\n\n**課題**\n- エラーハンドリングとかどうする？\n\t- エラーがあればすぐに落とす仕様にする？？？\n\n## Usage\n\n```python\n import os\n \n from commando import commando\n \n \n def myprint():\n     print("コマンドー")\n\n \n # コマンド文字列\n commando.add("mkdir test")\n # リスト形式のコマンド\n commando.add(["touch", "test\\\\test.txt"])\n\n # 独自定義の関数\n commando.add(myprint)\n \n # 追加した順でコマンドを実行\n commando.execute()\n```',
    'author': 'zztkm',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
