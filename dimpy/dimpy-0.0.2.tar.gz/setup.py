import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="dimpy", # Package Name
    version="0.0.2",
    author="Dwaipayan Deb",
    author_email="dwaipayandeb@yahoo.co.in",
    description="A package for creating N-dimensional list array",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dwaipayandeb/dimpy",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)