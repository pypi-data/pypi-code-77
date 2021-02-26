import setuptools

with open("./README.md", 'r') as f:
    readme = f.read()

with open('./requirements.txt', 'r') as f:
    requirements = [a.strip() for a in f]

import os
here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'rcute_scratch_link', 'version.py')) as f:
    ns = {}
    exec(f.read(), ns)
    version = ns['__version__']

setuptools.setup(
    name="rcute-scratch-link",
    version=version,
    author="Huang Yan",
    author_email="hyansuper@foxmail.com",
    description='scratch link for rcute robots',
    license="MIT",
    long_description='scratch link for rcute robots',
    long_description_content_type="text/markdown",
    url="https://github.com/r-cute/rcute-scratch-link",
    packages=['rcute_scratch_link'],
    install_requires=requirements,
    classifiers=(
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)