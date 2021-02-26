from setuptools import setup, find_packages

classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Developers',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]

with open("README.md") as fh:
    long_description = fh.read()

setup(
  name='ibl',
  version='0.0.5',
  description='Python api wrapper for infinity bot list',
  long_description_content_type="text/markdown",
  long_description=long_description,
  url='https://ibl.gitbook.io/ibl/',
  author='Andromeda',
  author_email='bots@rjbot.xyz',
  license='MIT',
  classifiers=classifiers,
  keywords='infinity bot list infinity-bot-list-python-api ibl',
  packages=find_packages(),
  install_requires=['aiohttp']
)
