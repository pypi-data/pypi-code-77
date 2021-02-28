# pylint: disable=line-too-long
'''
    :author: Pasquale Carmine Carbone

    Setup module
'''
import setuptools

with open('README.md', 'r') as fh:
    LONG_DESCRIPTION = fh.read()

setuptools.setup(
    setup_requires=['setuptools-git-version'],
    version_format='{tag}',
    name='python-polymorphism',
    author='Pasquale Carmine Carbone',
    author_email='pasqualecarmine.carbone@gmail.com',
    description='A simple utility library that allow you to use OOP Like Polymorphic Function in python',
    long_description=LONG_DESCRIPTION,
    url='https://github.com/KiraPC/python-polymorphism',
    long_description_content_type='text/markdown',
    packages=setuptools.find_packages(exclude=['venv', 'python-polymorphism.egg-info', 'build']),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development',
        'Typing :: Typed',
    ],
    python_requires='>=3.6'
)
