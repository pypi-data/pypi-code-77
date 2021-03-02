import setuptools

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setuptools.setup(
    name="python-bitcoin-test", # your package name
    version="0.2.8", # your package version
    author="alexzander", # package author
    author_email="just.python.mail.test@gmail.com", # package author email
    description="quick description", # package description
    long_description=long_description, # package long description
    long_description_content_type="text/markdown",
    url="",
    include_package_data=True,
    install_requires=[ # all installed 3rd party modules
        		"requests"
    ],
    platforms="any",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)