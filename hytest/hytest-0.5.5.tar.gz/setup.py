from setuptools import find_packages, setup
from os.path import join

from hytest.product import version

CLASSIFIERS = """
Development Status :: 4 - Beta
Intended Audience :: Developers
Topic :: Software Development :: Testing
License :: OSI Approved :: Apache Software License
Programming Language :: Python :: 3
Programming Language :: Python :: 3.6
Programming Language :: Python :: 3.7
Programming Language :: Python :: 3.8
Programming Language :: Python :: 3.9
""".strip().splitlines()

with open('README.md', encoding='utf8') as f:
    LONG_DESCRIPTION = f.read()

setup(
    name         = 'hytest',
    version      = version,
    author       = 'Patrik Jiang - Jiangchunyang',
    author_email = 'jcyrss@gmail.com',
    url          = 'http://www.python3.vip',
    download_url = 'https://pypi.python.org/pypi/hytest',
    license      = 'Apache License 2.0',
    description  = '一款系统测试自动化框架 Generic automation framework for QA testing',
    long_description = LONG_DESCRIPTION,
    keywords     = 'hytest automation testautomation',
    classifiers  = CLASSIFIERS,
    
    # https://docs.python.org/3/distutils/setupscript.html#listing-whole-packages    
    packages     = find_packages(),
    
    # https://docs.python.org/3/distutils/setupscript.html#installing-package-data
    package_data = {'hytest/utils': ['*.css','*.js']},
    
    include_package_data=True,
    
    install_requires=[   
          'rich',
          'dominate',
      ],
    entry_points = {
        'console_scripts': 
            [
                'hytest = hytest.run:run',
            ]
    }
)