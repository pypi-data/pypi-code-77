# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['mkdocstrings', 'mkdocstrings.handlers']

package_data = \
{'': ['*'],
 'mkdocstrings': ['templates/python/material/*',
                  'templates/python/readthedocs/*']}

install_requires = \
['Jinja2>=2.11,<3.0',
 'Markdown>=3.3,<4.0',
 'MarkupSafe>=1.1,<2.0',
 'mkdocs-autorefs>=0.1,<0.2',
 'mkdocs>=1.1,<2.0',
 'pymdown-extensions>=6.3,<9.0',
 'pytkdocs>=0.2.0,<0.12.0']

entry_points = \
{'mkdocs.plugins': ['mkdocstrings = mkdocstrings.plugin:MkdocstringsPlugin']}

setup_kwargs = {
    'name': 'mkdocstrings',
    'version': '0.15.0',
    'description': 'Automatic documentation from sources, for MkDocs.',
    'long_description': '# mkdocstrings\n\n[![ci](https://github.com/mkdocstrings/mkdocstrings/workflows/ci/badge.svg)](https://github.com/mkdocstrings/mkdocstrings/actions?query=workflow%3Aci)\n[![documentation](https://img.shields.io/badge/docs-mkdocs%20material-blue.svg?style=flat)](https://mkdocstrings.github.io/)\n[![pypi version](https://img.shields.io/pypi/v/mkdocstrings.svg)](https://pypi.org/project/mkdocstrings/)\n[![conda version](https://img.shields.io/conda/vn/conda-forge/mkdocstrings)](https://anaconda.org/conda-forge/mkdocstrings)\n[![gitter](https://badges.gitter.im/join%20chat.svg)](https://gitter.im/mkdocstrings/community)\n\nAutomatic documentation from sources, for [MkDocs](https://mkdocs.org/).\n\n---\n\n![mkdocstrings_gif1](https://user-images.githubusercontent.com/3999221/77157604-fb807480-6aa1-11ea-99e0-d092371d4de0.gif)\n\n---\n\n- [Features](#features)\n    - [Python handler features](#python-handler-features)\n- [Requirements](#requirements)\n- [Installation](#installation)\n- [Quick usage](#quick-usage)\n\n## Features\n\n- [**Language-agnostic:**](https://mkdocstrings.github.io/handlers/overview/)\n  just like *MkDocs*, *mkdocstrings* is written in Python but is language-agnostic.\n  It means you can use it with any programming language, as long as there is a\n  [**handler**](https://mkdocstrings.github.io/reference/handlers/base/) for it.\n  The [Python handler](https://mkdocstrings.github.io/handlers/python/) is built-in.\n  [Others](https://mkdocstrings.github.io/handlers/overview/) are external.\n  Maybe you\'d like to add another one to the list? :wink:\n\n- [**Multiple themes support:**](https://mkdocstrings.github.io/theming/)\n  each handler can offer multiple themes. Currently, we offer the\n  :star: [Material theme](https://squidfunk.github.io/mkdocs-material/) :star:\n  as well as basic support for the ReadTheDocs theme for the Python handler.\n\n- [**Cross-links across pages:**](https://mkdocstrings.github.io/usage/#cross-references)\n  *mkdocstrings* makes it possible to reference headings in other Markdown files with the classic Markdown linking\n  syntax: `[identifier][]` or `[title][identifier]` -- and you don\'t need to remember which exact page this object was\n  on. This works for any heading that\'s produced by a *mkdocstrings* language handler, and you can opt to include\n  *any* Markdown heading into the global referencing scheme.\n\n    **Note**: in versions prior to 0.15 *all* Markdown headers were included, but now you need to\n    [opt in](https://mkdocstrings.github.io/usage/#cross-references).\n\n- [**Inline injection in Markdown:**](https://mkdocstrings.github.io/usage/)\n  instead of generating Markdown files, *mkdocstrings* allows you to inject\n  documentation anywhere in your Markdown contents. The syntax is simple: `::: identifier` followed by a 4-spaces\n  indented YAML block. The identifier and YAML configuration will be passed to the appropriate handler\n  to collect and render documentation.\n\n- [**Global and local configuration:**](https://mkdocstrings.github.io/usage/#global-options)\n  each handler can be configured globally in `mkdocs.yml`, and locally for each\n  "autodoc" instruction.\n\n- [**Watch source code directories:**](https://mkdocstrings.github.io/usage/#watch-directories)\n  you can tell *mkdocstrings* to add directories to be watched by *MkDocs* when\n  serving the documentation, for auto-reload.\n\n- **Reasonable defaults:**\n  you should be able to just drop the plugin in your configuration and enjoy your auto-generated docs.\n\n### Python handler features\n\n- **Data collection from source code**: collection of the object-tree and the docstrings is done by\n  [`pytkdocs`](https://github.com/pawamoy/pytkdocs). The following features are possible thanks to it:\n    - **Support for type annotations:** `pytkdocs` collects your type annotations and *mkdocstrings* uses them\n      to display parameters types or return types.\n    - **Recursive documentation of Python objects:** just use the module dotted-path as identifier, and you get the full\n      module docs. You don\'t need to inject documentation for each class, function, etc.\n    - **Support for documented attribute:** attributes (variables) followed by a docstring (triple-quoted string) will\n      be recognized by `pytkdocs` in modules, classes and even in `__init__` methods.\n    - **Support for objects properties:** `pytkdocs` detects if a method is a `staticmethod`, a `classmethod`, etc.,\n      it also detects if a property is read-only or writable, and more! These properties will be displayed\n      next to the object signature by *mkdocstrings*.\n    - **Google-style sections support in docstrings:** `pytkdocs` understands `Arguments:`, `Raises:`\n      and `Returns:` sections, and returns structured data for *mkdocstrings* to render them.\n    - **reStructuredText-style sections support in docstrings:** `pytkdocs` understands all the\n      [reStructuredText fields](https://www.sphinx-doc.org/en/master/usage/restructuredtext/domains.html?highlight=python%20domain#info-field-lists),\n      and returns structured data for *mkdocstrings* to render them.\n      *Note: only RST **style** is supported, not the whole markup.*\n    - **Admonition support in docstrings:** blocks like `Note: ` or `Warning: ` will be transformed\n      to their [admonition](https://squidfunk.github.io/mkdocs-material/extensions/admonition/) equivalent.\n      *We do not support nested admonitions in docstrings!*\n    - **Support for reStructuredText in docstrings:** `pytkdocs` can parse simple RST.\n- **Every object has a TOC entry:** we render a heading for each object, meaning *MkDocs* picks them into the Table\n  of Contents, which is nicely display by the Material theme. Thanks to *mkdocstrings* cross-reference ability,\n  you can even reference other objects within your docstrings, with the classic Markdown syntax:\n  `[this object][package.module.object]` or directly with `[package.module.object][]`\n- **Source code display:** *mkdocstrings* can add a collapsible div containing the highlighted source code\n  of the Python object.\n\nTo get an example of what is possible, check *mkdocstrings*\'\nown [documentation](https://mkdocstrings.github.io/), auto-generated from sources by itself of course,\nand the following GIF:\n\n![mkdocstrings_gif2](https://user-images.githubusercontent.com/3999221/77157838-7184db80-6aa2-11ea-9f9a-fe77405202de.gif)\n\n## Roadmap\n\nSee the [Feature Roadmap issue](https://github.com/mkdocstrings/mkdocstrings/issues/183) on the bugtracker.\n\n## Requirements\n\n*mkdocstrings* requires Python 3.6 or above.\n\n<details>\n<summary>To install Python 3.6, I recommend using <a href="https://github.com/pyenv/pyenv"><code>pyenv</code></a>.</summary>\n\n```bash\n# install pyenv\ngit clone https://github.com/pyenv/pyenv ~/.pyenv\n\n# setup pyenv (you should also put these three lines in .bashrc or similar)\nexport PATH="${HOME}/.pyenv/bin:${PATH}"\nexport PYENV_ROOT="${HOME}/.pyenv"\neval "$(pyenv init -)"\n\n# install Python 3.6\npyenv install 3.6.12\n\n# make it available globally\npyenv global system 3.6.12\n```\n</details>\n\nThis project currently only works with the Material theme of MkDocs.\nTherefore, it is required that you have it installed.\n\n```\npip install mkdocs-material\n```\n\n## Installation\n\nWith `pip`:\n```bash\npython3.6 -m pip install mkdocstrings\n```\n\nWith `conda`:\n```bash\nconda install -c conda-forge mkdocstrings\n```\n\n## Quick usage\n\n```yaml\n# mkdocs.yml\ntheme:\n  name: "material"\n\nplugins:\n- search\n- mkdocstrings\n```\n\nIn one of your markdown files:\n\n```markdown\n# Reference\n\n::: my_library.my_module.my_class\n```\n\nSee the [Usage](https://mkdocstrings.github.io/usage) section of the docs for more examples!\n',
    'author': 'Timothée Mazzucotelli',
    'author_email': 'pawamoy@pm.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mkdocstrings/mkdocstrings',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
