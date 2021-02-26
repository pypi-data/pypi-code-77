# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aqbt',
 'aqbt.aquarium',
 'aqbt.aquarium.parsers',
 'aqbt.bioadapter',
 'aqbt.biopython',
 'aqbt.build_request',
 'aqbt.design',
 'aqbt.design.archived',
 'aqbt.design.components',
 'aqbt.design.dasi',
 'aqbt.design.dasi.dasi_to_aq',
 'aqbt.schema',
 'aqbt.sequence',
 'aqbt.utils']

package_data = \
{'': ['*'], 'aqbt.aquarium.parsers': ['data/*']}

install_requires = \
['bcbio-gff>=0.6.6,<0.7.0',
 'benchlingapi>=2.1.11,<3.0.0',
 'biopython>=1.78,<2.0',
 'colour>=0.1.5,<0.2.0',
 'dasi>=0.2.1,<0.3.0',
 'google-api-python-client>=1.7,<2.0',
 'google-auth-httplib2>=0.0.3,<0.0.4',
 'google-auth-oauthlib>=0.4.1,<0.5.0',
 'loggable-jdv>=0.1.7,<0.2.0',
 'networkx>=2.5,<3.0',
 'primer3plus>=1.0,<2.0',
 'pyblastbio>=0.9,<0.10',
 'pydent>=1.0.6,<2.0.0',
 'toml>=0.10.0,<0.11.0',
 'tqdm>=4.36,<5.0',
 'validators>=0.14.1,<0.15.0']

setup_kwargs = {
    'name': 'aqbt',
    'version': '0.0.1',
    'description': 'Aquarium strain builder tools',
    'long_description': "# Aquarium-SD2 Strain Builder Tools (aqbt)\n\nThis repo contains many Aquarium-related tools for constructing new engineered strains.\n\n**Features**\n\n* Automated design and Aquarium workflow submission of plasmid assemblies\n* Automated design and Aquarium workflow submission of yeast constructions\n* Conversion of Aquarium strain definitions to engineered GFF with FASTA.\n* JSON-schema validated serialization of Aquarium models\n* Aquarium <-> Benchling integration\n* Aquarium <-> SynBioHub integration (coming soon)\n* Common file type conversions GFF <> FASTA <> Genbank <> JSON <> Benchling <> Aq <> SBOL (planned)\n* Aquarium database faker for unit testing\n\n## Usage\n\n### Installation\n\n```\npip install .\n```\n\nInstall BLAST locally using the following:\n\n```\npyblast install\n```\n\n### Credentials\n\nAqBuildTools (aqbt) requires a `credentials.toml` file to connect with \nAquarium, Benchling and SynBioHub (coming soon). The following \ncreates the `default` scope for a aqbt session:\n```\n[aquarium.production]\nlogin = 'mylogin'\npassword = 'mypass'\nurl = 'http://aquarium.org'\n\n[benchling.production]\napikey = 'sk_398dfg983nsdfsdflksj'\ninitials = 'UWBF'\nschema = 'Aquarium DNA'\nprefix = 'aq'\nfolder_id = 'lib_ILUNzz6N'\nid = 'src_KE6uFvex'\n\n[session.default]\naquarium = 'production'\n```\n\n```python\nfrom aqbt import AquariumBuildTools\n\naqbt = AquariumBuildTools.from_toml('credentials.toml')\n```\n\n### Examples\n\n#### Querying the Aquarium server\n\n#### Connecting to Benchling and Synbiohub\n\n#### Plasmid construction\n\n#### Strain construction\n\n##### Generating GFFs\n\n## Related repos\n\n[trident](https://github.com/klavinslab/trident),\n[DASi](https://github.com/jvrana/DASi-DNA-Design),\n[Benchling API](https://github.com/klavinslab/benchling-api),\n[Terrarium](https://github.com/jvrana/Terrarium),\n[pyblast](https://github.com/jvrana/pyblast),\n[primer3-py-plus](https://github.com/jvrana/primer3-py-plus)\n",
    'author': 'Justin Vrana',
    'author_email': 'justin.vrana@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
