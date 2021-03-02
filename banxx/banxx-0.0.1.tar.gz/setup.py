import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="banxx",
    version="0.0.1",
    author="Ba Nguyễn",
    author_email="banx9x@gmail.com",
    description="Demo publish python module",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
)
