# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['certbot_dns_cloudns', 'certbot_dns_cloudns._internal']

package_data = \
{'': ['*']}

install_requires = \
['certbot>=1.12.0,<2.0.0',
 'cloudns-api>=0.9.3,<0.10.0',
 'dnspython>=2.1.0,<3.0.0',
 'zope.interface>=5.1.0,<6.0.0']

entry_points = \
{'certbot.plugins': ['dns-cloudns = '
                     'certbot_dns_cloudns._internal.authenticator:Authenticator']}

setup_kwargs = {
    'name': 'certbot-dns-cloudns',
    'version': '0.4.0',
    'description': 'ClouDNS DNS Authenticator plugin for Certbot',
    'long_description': 'The `certbot-dns-clounds` plugin automates the process of\ncompleting a ``dns-01`` challenge (`acme.challenges.DNS01`) by creating, and\nsubsequently removing, TXT records using the ClouDNS API.\n\nNamed Arguments\n---------------\n===================================== =====================================\n``--dns-cloudns-credentials``         ClouDNS credentials_ INI file.\n                                      `(Required)`\n``--dns-cloudns-propagation-seconds`` The number of seconds to wait for DNS\n                                      to propagate before asking the ACME\n                                      server to verify the DNS record.\n                                      `(Default: 60)`\n``--dns-cloudns-nameserver``          Nameserver used to resolve CNAME\n                                      aliases. (See the\n                                      `Challenge Delegation`_ section\n                                      below.)\n                                      `(Default: System default)`\n===================================== =====================================\n\nCredentials\n-----------\nUse of this plugin requires a configuration file containing the ClouDNS API\ncredentials.\n\n.. code-block:: ini\n\n   # Target user ID (see https://www.cloudns.net/api-settings/)\n   dns_cloudns_auth_id=1234\n   # Alternatively, one of the following two options can be set:\n   # dns_cloudns_sub_auth_id=1234\n   # dns_cloudns_sub_auth_user=foobar\n\n   # API password\n   dns_cloudns_auth_password=password1\n\nThe path to this file can be provided interactively or using the\n``--dns-cloudns-credentials`` command-line argument. Certbot records the\npath to this file for use during renewal, but does not store the file\'s\ncontents.\n\n.. caution::\n   You should protect your credentials, as they can be used to potentially\n   add, update, or delete any record in the target DNS server. Users who can\n   read this file can use these credentials to issue arbitrary API calls on\n   your behalf. Users who can cause Certbot to run using these credentials can\n   complete a ``dns-01`` challenge to acquire new certificates or revoke\n   existing certificates for associated domains, even if those domains aren\'t\n   being managed by this server.\n\nCertbot will emit a warning if it detects that the credentials file can be\naccessed by other users on your system. The warning reads "Unsafe permissions\non credentials configuration file", followed by the path to the credentials\nfile. This warning will be emitted each time Certbot uses the credentials file,\nincluding for renewal, and cannot be silenced except by addressing the issue\n(e.g., by using a command like ``chmod 600`` to restrict access to the file).\n\nChallenge Delegation\n--------------------\nThe dns-cloudns plugin supports delegation of ``dns-01`` challenges to\nother DNS zones through the use of CNAME records.\n\nAs stated in the `Let\'s Encrypt documentation\n<https://letsencrypt.org/docs/challenge-types/#dns-01-challenge>`_:\n\n    Since Let’s Encrypt follows the DNS standards when looking up TXT records\n    for DNS-01 validation, you can use CNAME records or NS records to delegate\n    answering the challenge to other DNS zones. This can be used to delegate\n    the _acme-challenge subdomain to a validation-specific server or zone. It\n    can also be used if your DNS provider is slow to update, and you want to\n    delegate to a quicker-updating server.\n\nThis allows the credentials provided to certbot to be limited to either a\nsub-zone of the verified domain, or even a completely separate throw-away\ndomain. This idea is further discussed in `this article\n<https://www.eff.org/deeplinks/2018/02/\ntechnical-deep-dive-securing-automation-acme-dns-challenge-validation>`_\nby the `Electronic Frontier Foundation <https://www.eff.org>`_.\n\nTo resolve CNAME aliases properly, Certbot needs to be able to access a public\nDNS server. In some setups, especially corporate networks, the challenged\ndomain might be resolved by a local server instead, hiding configured CNAME and\nTXT records from Certbot. In these cases setting the\n``--dns-cloudns-nameserver`` option to any public nameserver (e.g. ``1.1.1.1``)\nshould resolve the issue.\n\n\nExamples\n--------\n\n.. code-block:: bash\n\n   certbot certonly \\\n     --dns-cloudns \\\n     --dns-cloudns-credentials ~/.secrets/certbot/cloudns.ini \\\n     -d example.com\n\n.. code-block:: bash\n\n   certbot certonly \\\n     --dns-cloudns \\\n     --dns-cloudns-credentials ~/.secrets/certbot/cloudns.ini \\\n     -d example.com \\\n     -d www.example.com\n\n.. code-block:: bash\n\n   certbot certonly \\\n     --dns-cloudns \\\n     --dns-cloudns-credentials ~/.secrets/certbot/cloudns.ini \\\n     --dns-cloudns-propagation-seconds 30 \\\n     -d example.com\n\nSponsor\n-------\n\n.. image:: https://inventage.com/assets/img/logos/inventage-logo-farbig.svg\n  :target: https://inventage.com\n  :width: 400\n  :alt: Inventage AG\n',
    'author': 'Simon Marti',
    'author_email': 'simon.marti@inventage.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/inventage/certbot-dns-cloudns',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
