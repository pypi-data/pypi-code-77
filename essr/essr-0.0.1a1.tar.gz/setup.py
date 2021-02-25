import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="essr",
    version="0.0.1a1",
    author="Gaogle",
    author_email="byteleap@gmail.com",
    description="Electronic SSR",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/GaoangLiu/ssr",
    packages=setuptools.find_packages(),
    # py_modules=['dofast', 'argparse_helper', 'simple_parser', 'oss', 'config'],
    install_requires=[],
    entry_points={
        'console_scripts': ['essr=shadowsocksr.shadowsocks.local:main'],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
