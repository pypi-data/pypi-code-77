from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

setup(
    name='fit-cli',
    version='0.1.0',
    description='A command line utility for organizing directories of binary content.',
    long_description=readme,
    long_description_content_type='text/markdown',
    author='Jake Ledoux',
    author_email='contactjakeledoux@gmail.com',
    url='https://github.com/jakeledoux/fit-cli',
    license='GNU General Public License v2.0',
    packages=find_packages(exclude=('tests', 'docs')),
    install_requires=[
        'click>=7.1.2',
        'imageio>=2.9.0',
        'numpy>=1.20.1',
        'Pillow>=8.1.0',
        'SQLAlchemy>=1.3.23'
    ],
    entry_points='''
        [console_scripts]
        fit=fit.scripts.fit:cli
    '''
)
