# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lectern']

package_data = \
{'': ['*']}

install_requires = \
['beet>=0.10.4,<0.11.0', 'click>=7.1.2,<8.0.0', 'markdown-it-py>=0.6.2,<0.7.0']

entry_points = \
{'console_scripts': ['lectern = lectern.cli:main'],
 'pytest11': ['lectern = lectern.pytest_plugin']}

setup_kwargs = {
    'name': 'lectern',
    'version': '0.4.0',
    'description': 'Literate Minecraft data packs and resource packs.',
    'long_description': '<img align="right" src="https://raw.githubusercontent.com/mcbeet/lectern/main/logo.png?sanitize=true" alt="logo" width="52">\n\n# Lectern\n\n[![GitHub Actions](https://github.com/mcbeet/lectern/workflows/CI/badge.svg)](https://github.com/mcbeet/lectern/actions)\n[![PyPI](https://img.shields.io/pypi/v/lectern.svg)](https://pypi.org/project/lectern/)\n[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/lectern.svg)](https://pypi.org/project/lectern/)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)\n\n> Literate Minecraft data packs and resource packs.\n\n`@function tutorial:greeting`\n\n```mcfunction\nsay Hello, world!\n```\n\n## Introduction\n\nThis markdown file is interspersed with code fragments describing the content of a Minecraft data pack. Using `lectern`, you can turn this single file into an actual data pack that can be loaded into the game.\n\n**Features**\n\n- Turn markdown files into data packs and resource packs\n- Merge resources from several markdown files\n- Convert data packs and resource packs into markdown snapshots\n- Can be used as a [`beet`](https://github.com/mcbeet/beet) plugin\n- Highly extensible with custom directives\n- Automatically integrates with [`pytest-insta`](https://github.com/vberlier/pytest-insta)\n\n**Hmmkay but why?**\n\n- Editing data packs involves a lot of jumping around between files, for simple use-cases a single file is a lot easier to work with\n- Minecraft packs aggregate various types of files that can have complex interactions with each other, a literate style allows you to document these interactions fluently\n- Human-readable, single-file data pack and resource pack snapshots can be really useful to diff and track regressions in Minecraft-related tooling\n\n## Installation\n\nThe package can be installed with `pip`.\n\n```bash\n$ pip install lectern\n```\n\n## Getting started\n\nThis is an example of a markdown file that can be turned into a data pack:\n\n    # Beginner tutorial\n\n    Let\'s start by creating a simple function:\n\n    `@function tutorial:greeting`\n\n    ```mcfunction\n    say Hello, world!\n    ```\n\n    And now we can make it run when the data pack is loaded!\n\n    `@function_tag minecraft:load`\n\n    ```json\n    {\n      "values": ["tutorial:greeting"]\n    }\n    ```\n\nYou can use the `lectern` command-line utility to turn the markdown file into a data pack.\n\n```bash\n$ lectern tutorial.md --data-pack path/to/tutorial_data_pack\n```\n\nIf you\'re using [`beet`](https://github.com/mcbeet/beet) you can use `lectern` as a plugin in your pipeline.\n\n```json\n{\n  "pipeline": ["lectern"],\n  "meta": {\n    "lectern": {\n      "load": ["*.md"]\n    }\n  }\n}\n```\n\n## Directives\n\nData pack and resource pack fragments are code blocks, links or images annotated with a special `lectern` directive. Directives are prefixed with the `@` symbol and can be followed by zero or more arguments.\n\n```\n@<directive_name> <arg1> <arg2> <arg3>...\n```\n\n`lectern` provides directives for including namespaced resources inside data packs and resource packs. These built-in directives all expect a single argument specifying the fully-qualified resource name.\n\n```\n@function tutorial:greeting\n@function_tag minecraft:load\n```\n\nHere is a reference of all the supported resources:\n\n| Data pack                       |     | Resource pack      |     |\n| ------------------------------- | --- | ------------------ | --- |\n| `@advancement`                  |     | `@blockstate`      |     |\n| `@function`                     |     | `@model`           |     |\n| `@loot_table`                   |     | `@font`            |     |\n| `@predicate`                    |     | `@glyph_sizes`     | ⚠️  |\n| `@recipe`                       |     | `@truetype_font`   | ⚠️  |\n| `@structure`                    | ⚠️  | `@shader_post`     |     |\n| `@block_tag`                    |     | `@shader_program`  |     |\n| `@entity_type_tag`              |     | `@fragment_shader` |     |\n| `@fluid_tag`                    |     | `@vertex_shader`   |     |\n| `@function_tag`                 |     | `@text`            |     |\n| `@item_tag`                     |     | `@texture_mcmeta`  |     |\n| `@dimension_type`               |     | `@texture`         | ⚠️  |\n| `@dimension`                    |     |                    |     |\n| `@biome`                        |     |                    |     |\n| `@configured_carver`            |     |                    |     |\n| `@configured_feature`           |     |                    |     |\n| `@configured_structure_feature` |     |                    |     |\n| `@configured_surface_builder`   |     |                    |     |\n| `@noise_settings`               |     |                    |     |\n| `@processor_list`               |     |                    |     |\n| `@template_pool`                |     |                    |     |\n\n> ⚠️ Binary resources are supported but aren\'t compatible with code block fragments.\n\nThere are two additional built-in directives that can be used to include files using a path relative to the root of the data pack or the resource pack.\n\n```\n@data_pack pack.mcmeta\n@resource_pack pack.png\n@resource_pack assets/minecraft/textures/block/kelp_plant.png.mcmeta\n```\n\nThis is useful for adding files that aren\'t part of any particular namespace.\n\n## Code block fragments\n\nYou can include the content of a code block in a data pack or a resource pack by preceding it with a directive surrounded by backticks.\n\n`@function tutorial:greeting`\n\n```mcfunction\nsay Hello, world!\n```\n\nYou can put the directive in an html comment to make it invisible.\n\n<!-- @function_tag minecraft:load -->\n\n```json\n{\n  "values": ["tutorial:greeting"]\n}\n```\n\nThe directive can also be embedded directly inside the code block. You can insert a directive preceded by either `#` or `//` and the following lines will be included in the specified file.\n\n```mcfunction\n# @function tutorial:obtained_dead_bush\nsay You obtained a dead bush!\n```\n\nEmbedded directives are striped from the output. You can use multiple directives in a single code block.\n\n```json\n// @loot_table minecraft:blocks/diamond_ore\n{\n  "pools": [\n    {\n      "rolls": 1,\n      "entries": [\n        {\n          "type": "minecraft:item",\n          "name": "minecraft:dead_bush"\n        }\n      ]\n    }\n  ]\n}\n\n// @advancement tutorial:obtained_dead_bush\n{\n  "criteria": {\n    "dead_bush": {\n      "trigger": "minecraft:inventory_changed",\n      "conditions": {\n        "items": [\n          {\n            "item": "minecraft:dead_bush"\n          }\n        ]\n      }\n    }\n  },\n  "requirements": [\n    [\n      "dead_bush"\n    ]\n  ],\n  "rewards": {\n    "function": "tutorial:obtained_dead_bush"\n  }\n}\n```\n\n## Link fragments\n\nTODO\n\n## Image fragments\n\nTODO\n\n## Modifiers\n\nTODO\n\n## Command-line utility\n\n```bash\n$ lectern --help\nUsage: lectern [OPTIONS] [PATH]...\n\n  Literate Minecraft data packs and resource packs.\n\nOptions:\n  -d, --data-pack <path>       Extract data pack.\n  -r, --resource-pack <path>   Extract resource pack.\n  -e, --external-files <path>  Emit external files.\n  -v, --version                Show the version and exit.\n  -h, --help                   Show this message and exit.\n```\n\nYou can extract data packs from markdown files with the `-d/--data-pack` option. If the name ends with `.zip` the generated data pack will be zipped. Multiple markdown files can be merged together into a single data pack.\n\n```bash\n$ lectern demo.md --data-pack demo_data_pack\n$ lectern demo.md -d demo_data_pack\n$ lectern demo.md -d demo_data_pack.zip\n$ lectern foo.md bar.md -d demo_data_pack\n```\n\nThe `-r/--resource-pack` option lets you do exactly the same thing but with resource packs. The two options can be combined to extract a data packs and a resource pack at the same time.\n\n```bash\n$ lectern demo.md --resource-pack demo_resource_pack\n$ lectern demo.md -r demo_resource_pack\n$ lectern demo.md -d demo_data_pack -r demo_resource_pack\n```\n\nYou can also convert a combination of data packs and resource packs into a single markdown file.\n\n```bash\n$ lectern demo_data_pack demo.md\n$ lectern demo_data_pack.zip demo.md\n$ lectern demo_data_pack demo_resource_pack demo.md\n$ lectern foo_data_pack bar_data_pack demo.md\n```\n\nThe last argument is the name of the generated markdown file. By default, the `lectern` utility won\'t save the files that can\'t be directly defined inside the markdown file. You can use the `-o/--output-files` option to dump the files in the specified directory.\n\n```bash\n$ lectern demo_data_pack demo.md --output-files files\n$ lectern demo_data_pack demo.md -o files\n$ lectern demo_data_pack demo.md -o .\n```\n\n## Beet plugin\n\nTODO\n\n## Plain text documents\n\nTODO\n\n## Lectern for snapshot testing\n\nTODO\n\n## Contributing\n\nContributions are welcome. Make sure to first open an issue discussing the problem or the new feature before creating a pull request. The project uses [`poetry`](https://python-poetry.org).\n\n```bash\n$ poetry install\n```\n\nYou can run the tests with `poetry run pytest`.\n\n```bash\n$ poetry run pytest\n```\n\nThe project must type-check with [`pyright`](https://github.com/microsoft/pyright). If you\'re using VSCode the [`pylance`](https://marketplace.visualstudio.com/items?itemName=ms-python.vscode-pylance) extension should report diagnostics automatically. You can also install the type-checker locally with `npm install` and run it from the command-line.\n\n```bash\n$ npm run watch\n$ npm run check\n```\n\nThe code follows the [`black`](https://github.com/psf/black) code style. Import statements are sorted with [`isort`](https://pycqa.github.io/isort/).\n\n```bash\n$ poetry run isort lectern tests\n$ poetry run black lectern tests\n$ poetry run black --check lectern tests\n```\n\n---\n\nLicense - [MIT](https://github.com/mcbeet/lectern/blob/main/LICENSE)\n',
    'author': 'Valentin Berlier',
    'author_email': 'berlier.v@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mcbeet/lectern',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
