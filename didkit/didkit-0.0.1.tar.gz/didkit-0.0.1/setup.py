import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="didkit",
    version="0.0.1",
    author="Spruce Systems, Inc.",
    author_email="oss@spruceid.com",
    description="A toolkit for trusted interactions.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/spruceid/didkit",
    project_urls={
        "Bug Tracker": "https://github.com/spruceid/didkit/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
)
