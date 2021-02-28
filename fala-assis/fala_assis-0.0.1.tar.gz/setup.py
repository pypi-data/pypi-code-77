#-*- coding: utf-8 -*-
from setuptools import setup

with open("README.md", "r") as fh:
    readme = fh.read()

setup(name='fala_assis',
    version='0.0.1',
    url='https://github.com/OseiasBeu/AssistenteDeFala',
    license='MIT License',
    author='Oseias Beu',
    long_description=readme,
    long_description_content_type="text/markdown",
    author_email='oseiasbeu@outlook.com',
    keywords='Assistente de Fala',
    description=u'Assistente de fala que avisa um portador de deficiência visual quando o programa executou',
    packages=['fala_assis'],
    install_requires=['gtts','IPython'],)