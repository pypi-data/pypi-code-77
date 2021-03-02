import setuptools

from generate import generate

generate()

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="chameleongram",
    license="LGPLv3+",
    version="0.0.2",
    author="Davide Galilei",
    author_email="davidegalilei2018@gmail.com",
    description="An async (trio) MTProto Client written in Python 3",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/DavideGalilei/chameleongram",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        x.strip()
        for x in open("chameleongram/requirements.txt").read().splitlines()
        if x
    ],
)
