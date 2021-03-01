import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="longtext",
    version="0.0.1",
    author="Akash.A",
    description="Text line generator and repeater.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    py_modules=["longtext"],
    package_dir={'':'longtext'},
    install_requires=[]
)