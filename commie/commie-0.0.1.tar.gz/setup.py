from setuptools import setup, find_packages
from pathlib import Path

setup(
	name="commie",
	version="0.0.1",

	author="Art Galkin",
	author_email="ortemeo@gmail.com",
	url='https://github.com/rtmigo/commie.python',

	packages=find_packages(),
	install_requires=[],

	description="Finds comments in source code in different programming languages",

	long_description=(Path(__file__).parent/'README.md').read_text(),
	long_description_content_type='text/markdown',

  license='MIT',

	# entry_points={
  #       'console_scripts': [
  #           'allrights = allrights:main',
  #       ]},

	keywords=['comments', 'source code'],

	# https://pypi.org/classifiers/
	classifiers= [
		"Development Status :: 2 - Pre-Alpha",
		"Intended Audience :: Developers",
		'License :: OSI Approved :: MIT License',
    'Topic :: Software Development :: Documentation',
		"Programming Language :: Python :: 3.7",
		"Programming Language :: Python :: 3.8",
		"Programming Language :: Python :: 3.9",
	],

  test_suite='nose.collector',
  tests_require=['nose'],
  zip_safe=False
)