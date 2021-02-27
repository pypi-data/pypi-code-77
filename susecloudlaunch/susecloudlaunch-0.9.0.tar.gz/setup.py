# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['susecloudlaunch']

package_data = \
{'': ['*'],
 'susecloudlaunch': ['tf_templates/aws/*',
                     'tf_templates/azure/*',
                     'tf_templates/gcp/*']}

install_requires = \
['PyInquirer>=1.0.3,<2.0.0',
 'azure-mgmt-compute>=19.0.0,<20.0.0',
 'azure-mgmt-resource>=15.0.0,<16.0.0',
 'azure-mgmt-subscription>=1.0.0,<2.0.0',
 'boto3>=1.17.17,<2.0.0',
 'google-api-core>=1.26.0,<2.0.0',
 'google-api-python-client>=1.12.8,<2.0.0',
 'google-auth-httplib2>=0.0.4,<0.0.5',
 'google-auth>=1.27.0,<2.0.0',
 'google-cloud-core>=1.6.0,<2.0.0',
 'google-cloud-resource-manager>=0.30.3,<0.31.0',
 'googleapis-common-protos>=1.53.0,<2.0.0',
 'msrestazure>=0.6.4,<0.7.0',
 'oauth2client>=4.1.3,<5.0.0',
 'progress>=1.5,<2.0',
 'python-terraform>=0.10.1,<0.11.0']

setup_kwargs = {
    'name': 'susecloudlaunch',
    'version': '0.9.0',
    'description': '',
    'long_description': None,
    'author': 'Rich Paredes',
    'author_email': 'rich@suse.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
