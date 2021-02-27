import setuptools


with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name="xinet",
    version="0.0.7",
    author="Xinwei Liu",
    author_email="735613050@qq.com",
    description="Use Python to create and explor world.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/xinetzone/xinet",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)",
        "Operating System :: Microsoft :: Windows :: Windows 10",
        "Operating System :: POSIX :: Linux"
    ],
    python_requires='>=3.7',
)

