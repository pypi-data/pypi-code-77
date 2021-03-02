from setuptools import setup, find_packages
from os.path import join, dirname
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='pyFractaler',
    version='1.1',
    packages=find_packages(),
    long_description=long_description,
    entry_points={
        'console_scripts':
            ['fractal_demo = pyFractaler:demo']
        }
)