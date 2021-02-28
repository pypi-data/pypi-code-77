#!/usr/bin/env python
from setuptools import setup
import os
import pathlib
import words_count

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

setup(
    name='words-count',
    version=os.environ.get('RELEASE_VERSION', words_count.__version__),
    author='Javier Bravo',
    author_email='javibravo85@gmail.com',
    license="MIT",
    description="""CLI tool for that outputs the N (N by default 100) most common n-word (n by default is 3)
    sequence in text.""",
    long_description=README,
    long_description_content_type="text/markdown",
    keywords='count word words text',
    url='https://github.com/javibravo/words-count',
    packages=['words_count'],
    entry_points={
        'console_scripts': [
            'words-count=words_count.main:main'
        ],
    },
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Environment :: Console',
        'Natural Language :: English',
        'Operating System :: Unix',
        'Operating System :: MacOS',
        'License :: OSI Approved :: MIT License',
    ]
)
