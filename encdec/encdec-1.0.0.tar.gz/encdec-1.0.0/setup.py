from setuptools import setup

setup(name='encdec',
	version='1.0.0',
	description='A simple library to encrypt and decrypt content using Fernet.',
	author="Rehmat Alam",
	author_email="contact@rehmat.works",
	url="https://github.com/rehmatworks/rencdec",
	license="MIT",
	packages=[
		'encdec'
	],
	install_requires=[
		'cryptography'
	]
)