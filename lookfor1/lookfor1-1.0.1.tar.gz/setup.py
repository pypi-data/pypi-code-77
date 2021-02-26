from setuptools import setup, find_packages
from lookfor.__init__ import __version__

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='lookfor1',
    version=f'{__version__}',
    description='look for things',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Taylor Gamache',
    author_email='gamache.taylor@gmail.com',
    url='https://github.com/breakthatbass/lookfor',
    packages=find_packages(),
    license='MIT',
    install_requires=['termcolor'],
    entry_points={
        'console_scripts' : ['lf = lookfor.lookfor:main']
   }
)
