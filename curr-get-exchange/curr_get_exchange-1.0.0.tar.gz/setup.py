import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="curr_get_exchange",
    version="1.0.0",
    author="Jullies Onyango",
    author_email="Julliesnyash@gmail.com",
    description="Get Exchange Rate Between Different Currencies",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Jullies/Get-Exchange-Rate-Programatically",
    project_urls={
        "Bug Tracker": "https://github.com/Jullies/Get-Exchange-Rate-Programatically/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
)