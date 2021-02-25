import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="py_jdplayss",
    version="0.0.1",
    author="iessen",
    author_email="essen.wang@outlook.com",
    description="home-assistant skill api for Judian background Music player.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/iessen/py_jdplayss.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
