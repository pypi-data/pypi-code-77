import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ScuffedAPI",
    version="0.0.3",
    author="Pirxcy",
    description="Python wrapper for ScuffedAPI API.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/xMistt/ScuffedAPI-Wrapper",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
          'requests',
      ],
)
