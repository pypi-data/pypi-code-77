# -*- coding: utf-8 -*-
import re

import setuptools

project_url = "https://gitlab.com/w8jcik/dplot"

with open("README.md", "r") as fp:
    readme_content = fp.read()
    fixed_links = re.sub(r"!\[([^\]]*)\]\(([^)]*)\)", r"![\1]({}/-/raw/master/\2)".format(project_url), readme_content)

setuptools.setup(
    name="dplot",
    scripts=['dplot/bin/dplot'],
    version="0.0.3",
    author="Maciej Wójcik",
    author_email="w8jcik@gmail.com",
    description="Plots Gromacs SAXS, Pepsi-SAXS, Crysol and Debyer SWAXS intensity curves",
    long_description=fixed_links,
    long_description_content_type="text/markdown",
    url=project_url,
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
    ],
    install_requires=[
        'pandas',
        'seaborn',
        'matplotlib'
    ],
)
