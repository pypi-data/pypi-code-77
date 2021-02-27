from setuptools import setup

with open("README.md") as README:
    long_description = README.read()

setup(
    name='DidILeaveTheStoveOn',
    version='1.0',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Steven Shrewsbury',
    packages=['didileavethestoveon'],
    python_requires='>=3.6',
)
