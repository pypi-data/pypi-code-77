import os
from setuptools import setup

dir = os.path.dirname(__file__)

# long description from README file
with open('README.md', encoding='utf-8') as f:
    DESCRIPTION = f.read()

REQUIRED = open('requirements.txt').read()

setup(
    name='cryptoforecast_io_scraper',
    version='0.1.0',
    description='Simplified Pseudo API for CryptoForecast.io',
    long_description=DESCRIPTION,
    long_description_content_type='text/markdown',
    url='https://github.com/seekersoftec/cryptoforecast_io_scraper/',
    author=['Seekersoftec'],
    author_email='seekersoftec@gmail.com',
    license='Apache 2.0',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        "License :: OSI Approved :: MIT License",
    ],
    install_requires=REQUIRED,
    keywords='cryptoforecast.io scraper',
    packages=['cryptoforecast_io_scraper'],
)
