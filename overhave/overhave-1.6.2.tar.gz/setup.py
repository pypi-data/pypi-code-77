# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['overhave',
 'overhave.admin',
 'overhave.admin.flask',
 'overhave.admin.views',
 'overhave.admin.views.index',
 'overhave.cli',
 'overhave.cli.db',
 'overhave.db',
 'overhave.entities',
 'overhave.entities.authorization',
 'overhave.entities.authorization.manager',
 'overhave.entities.authorization.manager.ldap',
 'overhave.entities.feature',
 'overhave.entities.language',
 'overhave.entities.stash',
 'overhave.entities.stash.manager',
 'overhave.extra',
 'overhave.factory',
 'overhave.http',
 'overhave.http.base_client',
 'overhave.http.stash_client',
 'overhave.processing',
 'overhave.redis',
 'overhave.scenario',
 'overhave.storage',
 'overhave.testing',
 'overhave.testing.plugin_utils',
 'overhave.testing.plugin_utils.allure_utils',
 'overhave.utils']

package_data = \
{'': ['*'], 'overhave.admin': ['files/*', 'files/ace-src/*', 'templates/*']}

install_requires = \
['Flask-WTF>=0.14.2,<0.15.0',
 'Jinja2>=2.11.2,<3.0.0',
 'WTForms>=2.2,<3.0',
 'alembic>=1.4.3,<2.0.0',
 'click>=7.0,<8.0',
 'docker',
 'flask-admin>=1.5,<2.0',
 'flask-login>=0.4.1,<0.5.0',
 'gunicorn>=20.0.4,<21.0.0',
 'httptools>=0.1.1,<0.2.0',
 'ldap3>=2.6,<3.0',
 'psycopg2-binary>=2.8,<3.0',
 'pydantic-sqlalchemy>=0.0.6,<0.0.7',
 'pydantic>=1.7',
 'python-dateutil>=2.8.1,<3.0.0',
 'python-ldap>=3.2,<4.0',
 'pytz>=2019.1,<2020.0',
 'redis>=3.4.1,<4.0.0',
 'requests>=2.0.0',
 'sqlalchemy-utc==0.10.0',
 'sqlalchemy>=1.3.3,<2.0.0',
 'sqlalchemy_utils>=0.34.0,<0.35.0',
 'tenacity',
 'walrus>=0.8.0,<0.9.0',
 'wsgi_intercept>=1.8,<2.0',
 'yarl>=1.1.1,<2.0.0']

entry_points = \
{'console_scripts': ['overhave = overhave.cli:overhave',
                     'overhave-demo = demo:overhave_demo'],
 'pytest11': ['overhave = overhave.testing.plugin']}

setup_kwargs = {
    'name': 'overhave',
    'version': '1.6.2',
    'description': 'Overhave - web-framework for BDD',
    'long_description': '========\nOverhave\n========\n\n.. figure:: https://raw.githubusercontent.com/TinkoffCreditSystems/overhave/master/docs/includes/images/label_img.png\n  :width: 600\n  :align: center\n  :alt: Overhave framework\n\n  `Overhave`_ is the web-framework for BDD: scalable, configurable, easy to use, based on\n  `Flask Admin`_ and `Pydantic`_.\n\n  .. image:: https://github.com/TinkoffCreditSystems/overhave/workflows/CI/badge.svg\n    :target: https://github.com/TinkoffCreditSystems/overhave/actions?query=workflow%3ACI\n    :alt: CI\n\n  .. image:: https://img.shields.io/pypi/pyversions/overhave.svg\n    :target: https://pypi.org/project/overhave\n    :alt: Python versions\n\n  .. image:: https://img.shields.io/badge/code%20style-black-000000.svg\n    :target: https://github.com/TinkoffCreditSystems/overhave\n    :alt: Code style\n\n  .. image:: https://img.shields.io/pypi/v/overhave?color=%2334D058&label=pypi%20package\n    :target: https://pypi.org/project/overhave\n    :alt: Package version\n\n--------\nFeatures\n--------\n\n* Ready web-interface for easy BDD features management with `Ace`_ editor\n* Traditional Gherkin format for scenarios provided by `pytest-bdd`_\n* Execution and reporting of BDD features based on `PyTest`_  and `Allure`_\n* Auto-collection of `pytest-bdd`_ steps and display on the web-interface\n* Simple business-alike scenarios structure, easy horizontal scaling\n* Built-in wrappers for `pytest-bdd`_ hooks to supplement `Allure`_ report\n* Ability to create and use several BDD keywords dictionary with different languages\n* Versioning and deployment of scenario drafts to `Bitbucket`_\n* Built-in configurable management of users and groups permissions\n* Configurable strategy for user authorization, LDAP also provided\n* Database schema based on `SQLAlchemy`_ models and works with PostgreSQL\n* Still configurable as `Flask Admin`_, supports plug-ins and extensions\n* Distributed `producer-consumer` architecture based on Redis streams\n  through `Walrus`_ (partially integrated)\n* Web-browser emulation ability with custom toolkit (`GoTTY`_, for example)\n* Simple command-line interface, provided with `Click`_\n\n------------\nInstallation\n------------\n\nYou can install **Overhave** via pip from PyPI:\n\n.. code-block:: shell\n\n    pip install overhave\n\n--------\nOverview\n--------\n\nWeb-interface\n-------------\n\nThe web-interface is a basic tool for BDD features management. It consists of:\n\n* `Info` - index page with optional information about your tool or project;\n* `Scenarios` - section for features management, contains subsections\n    `Features`, `Test runs` and `Versions`:\n\n    * `Features`\n        gives an interface for features records management and provides info\n        about id, name author, time, editor and publishing status; it is possible\n        to search, edit or delete items through interface;\n    * `Test runs`\n        gives an interface for test runs management and provides info about\n\n        .. figure:: https://raw.githubusercontent.com/TinkoffCreditSystems/overhave/master/docs/includes/images/test_runs_img.png\n          :width: 500\n          :align: center\n          :alt: Script panel\n    * Versions\n        contains feature versions for corresponding to test runs.\n\n* `Access` - section for access management, contains `Users` and\n    `Groups` subsections;\n* `Emulation` - experimental section for alternative tools implementation\n    (in developing).\n\n**Overhave** features could be created and/or edited through special\n*script panel* in feature edit mode. Feature should have type registered by the\napplication, unique name, specified tasks list with the traditional format\n```PRJ-NUMBER``` and scenario text.\n\n**Script panel** has `pytest-bdd`_ steps table on the right side of interface.\nThese steps should be defined in appropriate fixture modules and registered\nat the application on start-up to be displayed.\n\n\n.. figure:: https://raw.githubusercontent.com/TinkoffCreditSystems/overhave/master/docs/includes/images/panel_img.png\n  :width: 600\n  :align: center\n  :alt: Script panel\n\n  Example of **Overhave** script panel in feature edit mode\n\nAllure report\n-------------\n\n**Overhave** generates `Allure`_ report after tests execution in web-interface.\nIf you execute tests manually through `PyTest`_, these results are could be\nconverted into the `Allure`_ report also with the `Allure CLI`_ tool.\nThis report contains scenarios descriptions as they are described in features.\n\n.. figure:: https://raw.githubusercontent.com/TinkoffCreditSystems/overhave/master/docs/includes/images/report_img.png\n  :width: 600\n  :align: center\n  :alt: Allure test-case report\n\n  Example of generated `Allure`_ report after execution of **Overhave**\'s feature\n\nCommand-line interface\n----------------------\n**Overhave** has a CLI that provides a simple way to start service web-interface,\nrun consumer and execute basic database operations. Examples are below:\n\n.. code-block:: shell\n\n    overhave db create-all\n    overhave admin --port 8080\n    overhave consumer -s EMULATION\n\n**Note**: service start-up takes a set of settings, so you can set them through\nvirtual environment with prefix ```OVERHAVE_```, for example ```OVERHAVE_DB_URL```.\nIf you want to configure settings in more explicit way through context injection,\nplease see next part of docs.\n\nContext injection\n-----------------\n\nContext setting\n^^^^^^^^^^^^^^^\n\nService could be configured via application context injection with prepared\ninstance of `OverhaveContext` object. This context could be set using\n```set_context``` function of initialized ```ProxyFactory``` instance.\n\nFor example, ```my_custom_context``` prepared. So, application start-up could\nbe realised with follow code:\n\n.. code-block:: python\n\n    from overhave import overhave_app, overhave_factory\n\n    factory = overhave_factory()\n    factory.set_context(my_custom_context)\n    overhave_app(factory).run(host=\'localhost\', port=8080, debug=True)\n\n**Note**:\n\n* ```overhave_app``` is the prepared `Flask` application with already enabled\n    Flask Admin and Login Manager plug-ins;\n* ```overhave_factory``` is a function for LRU cached instance of the **Overhave**\n    factory ```ProxyFactory```; the instance has an access to application components,\n    directly used in ```overhave_app```.\n* ```my_custom_context``` is an example of context configuration, see an\n    example code in `context_example.rst`_.\n\nImport context in PyTest\n^^^^^^^^^^^^^^^^^^^^^^^^\n\n**Overhave** has it\'s own built-in `PyTest`_ plugin, which is used to enable\nand configure injection of prepared context into application core instance.\nThe plugin provides two options:\n\n* `--enable-injection` - flag to enable context injection;\n\n* `--ctx-module` - option specifying path to Python module with context injection.\n\nThe module with context injection should contain usage of\n```set_context``` function, but this module should be\nunique and created only for `PyTest`_ usage instead of web-interface start-up.\n\nFor example, ```module_with_injection.py``` module contains:\n\n.. code-block:: python\n\n    from overhave import overhave_factory\n\n    overhave_factory().set_context(my_custom_context)\n\nAnd `PyTest` usage should be similar to:\n\n.. code-block:: bash\n\n    pytest --enable-injection --ctx-module=module_with_injection\n\nSpecified module will be imported before tests start-up (with\n```pytest_configure``` `PyTest`_ hook).\n\n\nFeatures structure\n------------------\n\n**Overhave** supports it\'s own special structure of features storage:\n\n.. image:: https://raw.githubusercontent.com/TinkoffCreditSystems/overhave/master/docs/includes/images/features_structure_img.png\n  :width: 400\n  :alt: Features structure example\n\n**Base features directory** could contain different feature types as\nseparate directories, each of them corresponds to predefined `pytest-bdd`_\nset of steps. It is possible to create your own horizontal structure of\ndifferent product directions with unique steps and `PyTest`_ fixtures.\n\n**Note**: this structure is used in **Overhave** application. The formed data\ngives a possibility to specify registered feature type in the web-interface\n*script panel*. Also, this structure defines which steps will be displayed in\nthe rigth side of *script panel*.\n\nFeature format\n--------------\n\n**Overhave** has it\'s own special feature\'s text format, which inherits\nGherkin from `pytest-bdd`_ with small updates:\n\n* required tag that is related to existing feature type directory, where\n    current feature is located;\n* info about feature - who is creator, last editor and publisher;\n* task tracker\'s tickets with traditional format ```PRJ-NUMBER```.\n\nAn example of filled feature content is located in\n`feature_example.rst`_.\n\nLanguage\n--------\n\nThe web-interface language is ENG by default and could not be switched\n(if it\'s necessary - please, create a ```feature request``` or contribute\nyourself).\n\nThe feature text as well as `pytest-bdd`_ BDD keywords are configurable\nwith **Overhave** extra models, for example RUS keywords are already defined\nin framework and available for usage:\n\n.. code-block:: python\n\n    from overhave.extra import RUSSIAN_PREFIXES, RUSSIAN_TRANSLIT_PACK\n\n    language_settings = OverhaveLanguageSettings(\n        step_prefixes=RUSSIAN_PREFIXES,\n        translit_pack=RUSSIAN_TRANSLIT_PACK\n    )\n\n**Note**: you could create your own prefix-value mapping for your language:\n\n.. code-block:: python\n\n    from overhave import StepPrefixesModel\n\n    GERMAN_PREFIXES = StepPrefixesModel(\n        FEATURE="Merkmal:",\n        SCENARIO_OUTLINE="Szenarioübersicht:",\n        SCENARIO="Szenario:",\n        BACKGROUND="Hintergrund:",\n        EXAMPLES="Beispiele:",\n        EXAMPLES_VERTICAL="Beispiele: Vertikal",\n        GIVEN="Gegeben ",\n        WHEN="Wann ",\n        THEN="Dann ",\n        AND="Und ",\n        BUT="Aber ",\n    )\n\nCustom index\n------------\n\n**Overhave** gives an ability to set custom index.html file for rendering. Path\nto file could be set through environment as well as set with context:\n\n.. code-block:: python\n\n    admin_settings = OverhaveAdminSettings(\n        index_template_path="/path/to/index.html"\n    )\n\n\nAuthorization strategy\n----------------------\n\n**Overhave** provides several authorization strategies, declared by\n```AuthorizationStrategy``` enum:\n\n* `Simple` - strategy without real authorization.\n    Every user could use preferred name. This name will be used for user\n    authority. Every user is unique. Password not required.\n\n* `Default` - strategy with real authorization.\n    Every user could use only registered credentials.\n\n* LDAP - strategy with authorization using remote LDAP server.\n    Every user should use his LDAP credentials. LDAP\n    server returns user groups. If user in default \'admin\' group or his groups\n    list contains admin group - user will be authorized. If user already placed\n    in database - user will be authorized too. No one password stores.\n\nAppropriate strategy and additional data should be placed into\n```OverhaveAuthorizationSettings```, for example LDAP strategy could be\nconfigured like this:\n\n.. code-block:: python\n\n    auth_settings=OverhaveAuthorizationSettings(\n        auth_strategy=AuthorizationStrategy.LDAP, admin_group="admin"\n    )\n\n\n------------\nContributing\n------------\n\nContributions are very welcome.\n\nPreparation\n-----------\n\nProject installation is very easy\nand takes just few prepared commands (`make pre-init` works only for Ubuntu;\nso you can install same packages for your OS manually):\n\n.. code-block:: shell\n\n    make pre-init\n    make init\n\nPackages management is provided by `Poetry`_.\n\nCheck\n-----\n\nTests can be run with `Tox`_. `Docker-compose`_ is used for other services\npreparation and serving, such as database. Simple tests and linters execution:\n\n.. code-block:: shell\n\n    docker-compose up -d db\n    make test\n    make lint\n\nPlease, see `make` file and discover useful shortcuts. You could run tests\nin docker container also:\n\n.. code-block:: shell\n\n    make test-docker\n\nDocumentation build\n-------------------\n\nProject documentation could be built via `Sphinx`_ and simple `make` command:\n\n.. code-block:: shell\n\n    make build-docs\n\nBy default, the documentation will be built using `html` builder into `_build`\ndirectory.\n\n-------\nLicense\n-------\n\nDistributed under the terms of the `GNU GPLv2`_ license.\n\n------\nIssues\n------\n\nIf you encounter any problems, please report them here in section `Issues`\nwith a detailed description.\n\n.. _`Overhave`: https://github.com/TinkoffCreditSystems/overhave\n.. _`Pydantic`: https://github.com/samuelcolvin/pydantic\n.. _`Flask Admin`: https://github.com/flask-admin/flask-admin\n.. _`Ace`: https://github.com/ajaxorg/ace\n.. _`PyTest`: https://github.com/pytest-dev/pytest\n.. _`pytest-bdd`: https://github.com/pytest-dev/pytest-bdd\n.. _`Allure`: https://github.com/allure-framework/allure-python\n.. _`Allure CLI`: https://docs.qameta.io/allure/#_get_started\n.. _`Bitbucket`: https://www.atlassian.com/git\n.. _`SQLAlchemy`: https://github.com/sqlalchemy/sqlalchemy\n.. _`Walrus`: https://github.com/coleifer/walrus\n.. _`GoTTY`: https://github.com/yudai/gotty\n.. _`GNU GPLv2`: http://www.apache.org/licenses/LICENSE-2.0\n.. _`Tox`: https://github.com/tox-dev/tox\n.. _`Poetry`: https://github.com/python-poetry/poetry\n.. _`Docker-compose`: https://docs.docker.com/compose\n.. _`Click`: https://github.com/pallets/click\n.. _`Sphinx`: https://github.com/sphinx-doc/sphinx\n.. _`context_example.rst`: https://github.com/TinkoffCreditSystems/overhave/blob/master/docs/includes/context_example.rst\n.. _`feature_example.rst`: https://github.com/TinkoffCreditSystems/overhave/blob/master/docs/includes/features_structure_example/feature_type_1/full_feature_example_en.feature',
    'author': 'Vladislav Mukhamatnurov',
    'author_email': 'livestreamepidemz@yandex.ru',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
