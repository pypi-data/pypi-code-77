import setuptools
from precipy import PRECIPY_VERSION

setuptools.setup(
    version=PRECIPY_VERSION,
    packages=setuptools.find_packages(),
    install_requires = [
        "jinja2",
        "markdown",
        "pygments"
        ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    scripts = ["bin/precipy"],
)
