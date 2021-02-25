import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Utility-logger-jma", # Replace with your own username
    version="0.0.1",
    author="Jinghan Ma",
    author_email="jinghan.m@helium10.com",
    description="A package for logging convenience",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jm-h10/utility_jma/utility_logger",
    project_urls={
        "Bug Tracker": "https://github.com/jm-h10/utility_jma/utility_logger"
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    python_requires='>=3.6',
)
