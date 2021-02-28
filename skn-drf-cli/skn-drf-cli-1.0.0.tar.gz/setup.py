import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

install_requires = [
    'click>=7.1,<7.2'
]

setuptools.setup(
    name="skn-drf-cli",
    version="1.0.0",
    author="Shayan Karimi",
    author_email="shayankarimi0078@gmail.com",
    description="Django Rest Framework command-line tools",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/shywn-mrk/drf-cli",
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=install_requires,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    entry_points= {
        "console_scripts": [
            "drf-cli = drf_cli.__main__:cli"
        ]
    }
)
