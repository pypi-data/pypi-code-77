# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tradehub']

package_data = \
{'': ['*']}

install_requires = \
['base58>=2.1.0,<3.0.0',
 'bech32>=1.2.0,<2.0.0',
 'ecdsa>=0.16.1,<0.17.0',
 'hdwallets>=0.1.2,<0.2.0',
 'jsons>=1.3.1,<2.0.0',
 'mnemonic>=0.19,<0.20',
 'requests>=2.25.1,<3.0.0',
 'web3>=5.15.0,<6.0.0']

setup_kwargs = {
    'name': 'tradehub',
    'version': '2.0.0',
    'description': 'Python Client to interact with the Switcheo Tradehub Blockchain to manage staking, liquidity pools, governance, and trading on Demex.',
    'long_description': '<p align="center">\n    <a href="https://scrutinizer-ci.com/g/Mai-Te-Pora/tradehub-python/">\n        <img src="https://img.shields.io/scrutinizer/quality/g/mai-te-pora/tradehub-python/main" alt="Code Quality"></a>\n    <a href="https://app.codecov.io/gh/Mai-Te-Pora/tradehub-python/">\n        <img src="https://img.shields.io/codecov/c/github/mai-te-pora/tradehub-python" alt="Code Coverage"></a>\n    <a href="https://libraries.io/github/Mai-Te-Pora/tradehub-python" alt="Dependcy Status">\n        <img src="https://img.shields.io/librariesio/github/Mai-Te-Pora/tradehub-python">\n    <a href="https://pypi.org/project/tradehub/">\n        <img src="https://img.shields.io/pypi/v/tradehub" alt="PyPi Version"/></a>\n    <a href="https://pypi.org/project/tradehub/#history">\n        <img src="https://img.shields.io/pypi/pyversions/tradehub"/></a>\n</p>\n<p align="center">\n    <a href="https://github.com/Mai-Te-Pora/tradehub-python/blob/main/LICENSE" alt="License">\n        <img src="https://img.shields.io/github/license/mai-te-pora/tradehub-python" /></a>\n    <a href="https://github.com/Mai-Te-Pora/tradehub-python/graphs/contributors" alt="Contributors">\n        <img src="https://img.shields.io/github/contributors/Mai-Te-Pora/tradehub-python" /></a>\n    <a href="https://github.com/Mai-Te-Pora/tradehub-python/pulse" alt="Commit Activity">\n        <img src="https://img.shields.io/github/commit-activity/m/mai-te-pora/tradehub-python" /></a>\n    <a href="https://github.com/Mai-Te-Pora/tradehub-python/issues">\n        <img src="https://img.shields.io/github/issues/mai-te-pora/tradehub-python" alt="Open Issues"></a>\n    <a href="">\n        <img src="https://img.shields.io/pypi/dm/tradehub" alt="Downloads"></a>\n</p>\n\n# Tradehub Python API\n\nThis repository is designed to easily integrate your Python code or application with the Switcheo Tradehub Blockchain. This API is designed to interact with the decentralized network of Validators designed to keep the blockchain running and secure. This allows you to choose trusted endpoints or select random endpoints to interact with.\n\nThis project has been submitted on the Switcheo Foundation forums as part of the wider Switcheo community and you can follow official progress in this thread: https://forum.switcheo.foundation/topic/49/python-sdk-for-tradehub\n\n**NOTE:** This repository and underlying blockchain is under active development and may change drastically from each update.\n\nIf you have ideas or contributions we are accepting Pull Requests.\n\n## Getting Started\n\n```\npip install tradehub\n```\n\nOr Using Poetry - https://python-poetry.org/\n\n```\npoetry add tradehub\n```\n\n## Documentation\n\nThe documentation site can be found at: https://mai-te-pora.github.io/tradehub-python/\n\n### Examples and Tests\n\nWe have provided examples and tests (unittests) for the majority of the functions available across this project. We are always looking for help with this because having tests pass has proven to be the most difficult part of this project.\n\n## Usage\n\nThere are many clients to choose from and depending on your needs there are only one or two you should mainly interact with because most of these inheret from the building blocks.\n\nTraders should use the `Demex Client`\nValidators could use the `Demex Client` but combining the `Wallet` Client and `Authenticated Client` together is effectively the same.\n\nThe way these classes inheret from each other is as follows (top level first):\n\n<p style="text-align: center;">\nDemex Client</br>\n:arrow_up:</br>\nAuthenticated Client     +     Wallet</br>\n:arrow_up:</br>\nTransactions Client</br>\n:arrow_up:</br>\nPublic Client</br>\n:arrow_up:</br>\nPublic Blockchain Client</br>\n:arrow_up:</br>\nNetwork Crawler Client</br>\n</p>\n\n### Demex Client\n\nThis client utilizes all the other clients and can call wallet, authenticated, and public endpoints.\n\n```\nfrom tradehub.demex_client import DemexClient\n\ndemex_crawl = DemexClient(mnemonic=mnemonic, network="mainnet", trusted_ips=None, trusted_uris=None)\ndemex_ips = DemexClient(mnemonic=mnemonic, network="mainnet", trusted_ips=["54.255.5.46", "175.41.151.35"], trusted_uris=None)\ndemex_uris = DemexClient(mnemonic=mnemonic, network="mainnet", trusted_ips=None, trusted_uris=["http://54.255.5.46:5001", "http://175.41.151.35:5001"])\n```\n\n`demex_crawl` will crawl the Tradehub network for active validators to interact with. There is ~5 second startup time to perform this but if you are running a long running process this should be acceptable.\n`demex_ips` will respond very quickly as we are assuming trust and only checking that they have their persistence service turned on, can be used for quick interaction or lookups.\n`demex_uris` similar to `demex_ips`, can be used for quick interaction or lookups.\n\n#### Wallet\n\n```\ndemex_ips.wallet.address\n```\n\n#### Authenticated Client\n\n```\ndemex_ips.tradehub.send_tokens()\n```\n\n#### Public Client\n\n```\ndemex_ips.tradehub.get_all_validators()\n```\n',
    'author': 'Your Name',
    'author_email': 'you@example.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Mai-Te-Pora/tradehub-python',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
