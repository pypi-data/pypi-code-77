import setuptools

with open("README.md", "r") as fh:
  long_description = fh.read()

setuptools.setup(
    name="pyobe",
    version="0.0.1",
    author="Jannchie",
    author_email="jannchie@gmail.com",
    description="Probe system for crawl data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Jannchie/pyobe",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
