from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="btse-python",
    version="0.0.1",
    author="Yottatix",
    author_email="st@yottatix.com",
    description="Python module to connect to btse.com",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yottatix/btse-python",
    project_urls={
        "Bug Tracker": "https://github.com/yottatix/btse-python/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(exclude=['tests', 'tests.*']),
    install_requires=['requests'],
    python_requires='>=3.6',
)
