# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bucket_dir']

package_data = \
{'': ['*'], 'bucket_dir': ['templates/*']}

install_requires = \
['Jinja2>=2.11.3,<3.0.0',
 'boto3>=1.17.11,<2.0.0',
 'humanize>=3.2.0,<4.0.0',
 'rich>=9.11.0,<10.0.0']

entry_points = \
{'console_scripts': ['bucket-dir = bucket_dir:run_cli']}

setup_kwargs = {
    'name': 'bucket-dir',
    'version': '0.4.1',
    'description': 'Generate directory listings for S3 statically hosted content.',
    'long_description': '\n# bucket-dir\n\n**bucket-dir** is a utility for generating a browsable directory tree for an AWS S3 bucket.\n\n!["Sample"](/docs/sample.png "A sample of bucket-dir output.")\n\nIt was built in order to host Maven and Ivy repositories in S3 and serve them via CloudFront, but it could meet other needs too.\n\n> DISCLAIMER: This utility is the product of a time boxed spike. It should not be considered production ready. Use at your own risk.\n\n## Installation\n\nThe **bucket-dir** wheel is not currently hosted anywhere. You\'ll need to clone the repository. You then have two options.\n\n### Build and install a wheel\n\nIn order to install, first run `make build` to produce a `.whl` package. It will be created within a `dist` folder.\n\nOnce you have built the wheel, setup a virtual environment with a version of python newer than 3.8 and install with:\n\n```\npip install /path/to/repo/dist/bucket_dir-0.1.2-py3-none-any.whl\n```\n\n### Use the local bucket-dir script\n\nInstead of building, you can use the provided `bucket-dir` script from the root of the repo. Keep in mind that you\'ll need to provide a path, e.g. `./bucket-dir --help`.\n\n## Usage\n\nRun `bucket-dir` with the name of the bucket you wish to index as a parameter:\n\n```\nbucket-dir foo-bucket\n```\n\nUse `bucket-dir --help` for all arguments.\n\nBe sure to provide the command with credentials that allow it to perform ListBucket and PutObject calls against the bucket. E.g. with [aws-vault](https://github.com/99designs/aws-vault):\n\n```\naws-vault exec foo-profile -- bucket-dir foo-bucket\n```\n\n## Development\n\nSee the `Makefile` and run the appropriate rules.\n\n## License\n\nThis code is open source software licensed under the [Apache 2.0 License]("http://www.apache.org/licenses/LICENSE-2.0.html").\n',
    'author': 'Dave Randall',
    'author_email': '19395688+daveygit2050@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/hmrc/bucket-dir',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
