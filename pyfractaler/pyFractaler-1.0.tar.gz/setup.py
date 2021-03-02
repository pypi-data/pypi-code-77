from setuptools import setup, find_packages
from os.path import join, dirname

setup(
    name='pyFractaler',
    version='1.0',
    packages=find_packages(),
    long_description=open(join(dirname(__file__), 'README.txt')).read(),
    entry_points={
        'console_scripts':
            ['fractal_demo = __init__:demo',
             'fractal_demo_ruled = __init__:demo_ruled']
        }
)