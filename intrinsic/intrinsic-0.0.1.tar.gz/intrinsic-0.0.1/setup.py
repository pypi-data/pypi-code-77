import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="intrinsic", # Replace with your own username
    version="0.0.1",
    author="Oleg Kachan",
    author_email="oleg.n.kachan@gmail.com",
    description="Intrinsic Dimension Estimation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/oleg-kachan/intrinsic",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
