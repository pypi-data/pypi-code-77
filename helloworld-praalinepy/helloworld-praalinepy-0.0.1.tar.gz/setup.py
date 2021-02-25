from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='helloworld-praalinepy',
    version='0.0.1',
    description='Hello world for python packaging',
    url="https://www.praaline.org",
    author="George Christodoulides",
    author_email="george@mycontent.gr",
    py_modules=["helloworld"],
    package_dir={'' : 'src'},
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)",
        "Operating System :: OS Independent",
    ],
    long_description=long_description,
    long_description_content_type="text/markdown",
    extras_require = {
        "dev": [
            "pytest>=3.7",
        ],
    },
)

