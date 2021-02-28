# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pwnedpasswords_offline', 'pwnedpasswords_offline.tools']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pwnedpasswords-offline',
    'version': '1.0.3',
    'description': 'Pwned Passwords check (offline)',
    'long_description': '# Pwned Passwords check (offline)\n\n![PyPI](https://img.shields.io/pypi/v/pwnedpasswords-offline)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\n## Quickstart\n\n * Download "SHA-1" version "(ordered by hash)" from https://haveibeenpwned.com/Passwords\n * Extract file, yielding `pwned-passwords-sha1-ordered-by-hash-v7.txt` (for current version 7)\n\n## Simple usage\n````python\nfrom pwnedpasswords_offline import PwnedPasswordsOfflineChecker\nif PwnedPasswordsOfflineChecker("data/pwned-passwords-sha1-ordered-by-hash-v7.txt").lookup_raw_password("Password1!"):\n    print("Pwned!")\n````\n\n## Batch usage\nYou can also pre-open the database file, especially if you\'re checking multiple passwords in bulk:\n\n````python\nfrom pwnedpasswords_offline import PwnedPasswordsOfflineChecker\nchecker = PwnedPasswordsOfflineChecker("data/pwned-passwords-sha1-ordered-by-hash-v7.txt")\nchecker.open()\nfor password in ["Password1!", "correct horse battery staple", "actress stapling driver placidly swivel doorknob"]:\n    if checker.lookup_raw_password(password):\n        print(f"\'{password}\' is pwned!")\nchecker.close()\n````\n\nYou should not forget to call `.close()` after you\'re done.\n\n## As context manager\n\nYou can use the object as a context manager to automatically open and close it:\n\n`````python\nfrom pwnedpasswords_offline import PwnedPasswordsOfflineChecker\nwith PwnedPasswordsOfflineChecker("data/pwned-passwords-sha1-ordered-by-hash-v7.txt") as checker:\n    for password in ["Password1!", "correct horse battery staple", "actress stapling driver placidly swivel doorknob"]:\n        if checker.lookup_raw_password(password):\n            print(f"\'{password}\' is pwned!")\n`````\n\n## Check hash directly\n\nInstead of calling `.lookup_raw_password()` you can call `.lookup_hash()` if you already have the plain SHA-1 hash:\n\n````python\nfrom pwnedpasswords_offline import PwnedPasswordsOfflineChecker\nif PwnedPasswordsOfflineChecker("data/pwned-passwords-sha1-ordered-by-hash-v7.txt").lookup_hash("32CA9FD4B3F319419F2EA6F883BF45686089498D"):\n    print("Pwned!")\n````\n',
    'author': 'Henryk Plötz',
    'author_email': 'henryk@ploetzli.ch',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/henryk/pwnedpasswords-offline',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
