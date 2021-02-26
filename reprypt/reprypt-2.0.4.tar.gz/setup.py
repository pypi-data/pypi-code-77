from setuptools import setup
from os.path import exists


requires = []
long_description = open("readme.md").read() if exists("readme.md") else ""


setup(
    name='reprypt',
    version='2.0.4',
    description='Encryption Module',
    url='https://github.com/tasuren/reprypt',
    author='tasuren',
    author_email='tasuren5@gmail.com',
    license='MIT',
    keywords='encrypt decrypt',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=[
        "reprypt"
    ],
    install_requires=requires,
    classifiers=[
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)