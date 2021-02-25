# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['devdata', 'devdata.management', 'devdata.management.commands']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'django-devdata',
    'version': '0.1.4',
    'description': '',
    'long_description': '# django-devdata\n\n`django-devdata` provides a convenient workflow for creating development\ndatabases seeded with anonymised production data. Have a development database\nthat contains useful data, and is fast to create and keep up to date.\n\n#### Problem\n\nIn the same way that development environments being close in configuration to\nproduction environments, it\'s important that the data in databases we use for\ndevelopment is a realistic representation of that in production.\n\nOne option is to use a dump of a production database, but there are several\nproblems with this:\n\n1. This is bad for user privacy, and therefore a security risk. It may not be\n   allowed in some organisations.\n2. It\'s a limiting factor once the production database is too big to fit on a\n   development computer.\n3. Processes to take a sample of data from a database need to preserve\n   referential integrity.\n4. It limits test data to the data available in production.\n\nAnother option is to use factories or fake data to generate the entire\ndevelopment database. This is mostly desirable, but...\n\n- It can be a burden to maintain factories once there are hundreds or thousands\n  of them.\n- It can be hard to retroactively add these to a Django site of a significant\n  size.\n\n#### Solution\n\n`django-devdata` provides defines a three step workflow:\n\n1. _Exporting_ data, with a customisable export strategies per model.\n2. _Anonymising_ data, with customisable anonymisation per field/model.\n3. _Importing_ data, with customisable importing per model.\n\n`django-devdata` ships with built-in support for:\n\n- Exporting full tables\n- Exporting subsets (random, latest, specified primary keys)\n- Anonymising data with [`faker`](https://github.com/joke2k/faker/)\n- Importing exported data\n- Importing data from [`factory-boy`](https://github.com/FactoryBoy/factory_boy)\n  factories\n\nExporting, anonymising, and importing, are all configurable, and\n`django-devdata`\'s base classes will help do this without much work.\n\n## Workflow\n\n#### Exporting\n\nThis step allows a sync strategy to persist some data that will be used to\ncreate a new development database. For example, the `QuerySetStrategy` can\nexport data from a table to a filesystem for later import.\n\nThis can be used for:\n\n- Exporting a manually created database for other developers to use.\n- Exporting realistic data from a production database.\n- A cron job to maintain a development dataset hosted on cloud storage.\n\nThis step is optional (the built-in factory strategy doesn\'t do this).\n\n#### Anonymisation\n\nThis step is critical when using `django-devdata` to export from production\nsources. It\'s not a distinct step, but rather an opt-out part of the export\nstep.\n\n#### Importing\n\nThis step is responsible for creating a new database and filling it. If any\nexporting strategies have been used those must have run first, or their outputs\nmust have been downloaded if they are being shared/hosted somewhere.\n\nFactory-based strategies generate data during this process.\n\n## Customising\n\n#### Strategies\n\nThe `django-devdata` strategies define how an import and optionally an export\nhappen. Each model is configured with a list of Strategies to use.\n\nClasses are provided to inherit from for customising this behaviour:\n\n- `Strategy` – the base class of all strategies.\n- `Exportable` –\xa0a mixin that opts this strategy in to the export step.\n- `QuerySetStrategy` – the base of all strategies that export production data\n  to a filesystem. Handles referential integrity, serialisation, and\n  anonymisation of the data pre-export.\n- `FactoryStrategy` – the base of all strategies that create data based on\n  `factory-boy` factories.\n\nThe API necessary for classes to implement is small, and there are customisation\npoints provided for common patterns.\n\nIn our experience most models can be exported with just the un-customised\n`QuerySetStrategy`, some will need to use other pre-provided strategies, and\na small number will need custom exporters based on the classes provided.\n\n#### Anonymisers\n\nAnonymisers are configured by field name, and by model and field name.\n\nEach anonymiser is a function that takes a number of kwargs with useful context\nand returns a new value, compatible with the Django JSON encoder/decoder.\n\nThe signature for an anonymiser is:\n\n```python\ndef anonymise(*, obj: Model, field: str, pii_value: Any, fake: Faker) -> Any:\n    ...\n```\n\nThere are several anonymisers provided to use or to build off:\n\n- `faker_anonymise` – Use `faker` to anonymise this field with the provided\n  generator, e.g. `faker_anonymise(\'pyint\', min_value=15, max_value=85)`.\n- `const` – anonymise to a constant value, e.g. `const(\'ch_XXXXXXXX\')`.\n- `random_foreign_key` –\xa0anonymise to a random foreign key.\n\n`django-devdata`\'s anonymisation is not intended to be perfect, but rather to be\na reasonable default for creating useful data that does a good enough job by\ndefault. _Structure_ in data can be used to de-anonymise users in some cases\nwith advanced techniques, and `django-devdata` does not attempt to solve for\nthis case as most attackers, users, and legislators, are more concerned about\nobviously personally identifiable information such as names and email addresses.\nThis anonymisation is no replacement for encryption at-rest with tools like\nFileVault or BitLocker on development machines.\n\nAn example of this pragmatism in anonymisation is the `preserve_nulls` argument\ntaken by some built-in anonymisers. This goes against _true_ anonymisation, but\nthe absence of data is typically not of much use to attackers (or concern for\nusers), if the actual data is anonymised, while this can be of huge benefit to\ndevelopers in maintaining data consistency.\n\n#### Settings\n\n`django-devdata` makes heavy use of Django settings for both defining how it\nshould act for your site, and also for configuring how you\'ll use your workflow.\n\n```python\n"""\ndjango-devdata default settings, with documentation on usage.\n"""\n\n# Required\n# A mapping of app model label to list of strategies to be used.\nDEVDATA_STRATEGIES = ...\n# {\'auth.User\': [QuerySetStrategy(name=\'all\')], \'sessions.Session\': []}\n\n# Optional\n# A mapping of field name to an anonymiser to be used for all fields with that\n# name.\nDEVDATA_FIELD_ANONYMISERS = {}\n# {\'first_name\': faker_anonymise(\'first_name\'), \'ip\': const(\'127.0.0.1\')}\n\n# Optional\n# A mapping of app model label to a mapping of fields and anonymisers to be\n# scoped to just that model.\nDEVDATA_MODEL_ANONYMISERS = {}\n# {\'auth.User\': {\'first_name\': faker_anonymise(\'first_name\')}}\n\n# Required if using any exportable strategies.\n# The full path to the directory in which to store any exported data.\nDEVDATA_LOCAL_DIR = ...\n\n# Required\n# Command to run for psql, used for importing only. If psql is on the path in\n# your development environment no change is needed.\nDEVDATA_PSQL_COMMAND = \'psql\'\n\n# Required\n# Command to run for pg_dump, used for exporting the schema and migrations only.\n# If running the export on the same machine as the database this can be left\n# unchanged, but typically this will need changing.\nDEVDATA_PGDUMP_COMMAND = \'pg_dump\'\n# \'pg_dump -h my-database-host.local -u my-user\'\n# \'ssh me@production pg_dump\'\n\n# Optional\n# Command to run for QuerySetStrategy if exporting from another machine or\n# directory. If `None`, by default, no extra process is created, but if\n# provided, this command is used in a sub process. If overridden, this will\n# typically be a call to `devdata_dump`, but that management command may be\n# overridden itself so as long as the same arguments can be passed this can be\n# anything.\nDEVDATA_DUMP_COMMAND = None\n# \'ssh me@production /opt/my-app/manage.py devdata_dump\'\n\n# Optional\n# List of locales to be used for Faker in generating anonymised data.\nDEVDATA_FAKER_LOCALES = None\n# [\'en_GB\', \'en_AU\']\n```\n',
    'author': 'Dan Palmer',
    'author_email': 'dan@danpalmer.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/danpalmer/django-devdata',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
}


setup(**setup_kwargs)
