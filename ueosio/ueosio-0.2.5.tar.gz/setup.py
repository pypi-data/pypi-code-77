# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ueosio']

package_data = \
{'': ['*']}

install_requires = \
['base58>=2.0.0,<3.0.0', 'cryptos>=1.36,<2.0', 'requests>=2.23.0,<3.0.0']

setup_kwargs = {
    'name': 'ueosio',
    'version': '0.2.5',
    'description': 'uEOSIO python library',
    'long_description': '# µEOSIO\n**General purpose library for the EOSIO blockchains**\n\nMicro EOSIO allows you to interact with any EOSio chain using Python, it consists of 3 modules: \n\n* **DS:** Is the Data Stream module and it contains functions for serialization and deserialization of data streams in the eosio format.\n* **UTILS:** General functions that are useful for eosio.\n* **RPC:** Module for making API interactions.\n* **ABI:** Module to work with eosio ABI files\n\n# Install\n\n    pip3 install ueosio\n\n# Build from source\n\n    git clone https://github.com/EOSArgentina/ueosio\n    cd ueosio\n    python3 -m venv venv\n    source venv/bin/activate\n    pip3 install -r examples/requirements.txt\n\n### Examples:\n\n[tx.py](/examples/tx.py): Send a transaction on any given chain.\n\n[keys.py](/examples/keys.py): Generate a key pair or get the public key of any given private key.\n\n[approve_multisig.py](/examples/approve_multisig.py): Approve a multisig transaction.\n\n[create_account.py](/examples/create_account.py): Create an account, buy ram and delegate bandwidth and CPU. \n\n[get_top_10_bps.py](/examples/get_top_10_bps.py): Use the rpc module to get list of BPs on any eosio blockchain. \n\n[abi_hash.py](/examples/abi_hash.py): Get serialized abi hash. \n\n[extract_pubkey_from_tx.py](/examples/extract_pubkey_from_tx.py): Extract pubkeys used to sign a transaction. \n_____\n\n\n[MIT License](LICENSE) \\\nCopyright (c) 2020 EOS Argentina\n',
    'author': 'Matias Romeo',
    'author_email': 'matias.romeo@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/EOSArgentina/ueosio',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
