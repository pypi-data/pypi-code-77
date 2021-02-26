from setuptools import setup, find_packages
from os import path

with open(path.join(".", 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
      name='jSona',
      version=3.1,
      license='MIT',
      author='oimq',
      author_email='taep0q@gmail.com',
      url='https://github.com/oimq/jSona',
      description='JSON format handler on the json built-in module',
      long_description=long_description,
      long_description_content_type="text/markdown",
      packages=find_packages(),
      install_requires=[],
      zip_safe=False,
      classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent"
      ],
)