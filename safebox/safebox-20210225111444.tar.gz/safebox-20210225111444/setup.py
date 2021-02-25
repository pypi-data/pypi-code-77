import datetime
import os
from setuptools import setup, find_packages
from distutils.extension import Extension
from Cython.Build import cythonize


sources = ["./safebox/safebox.pyx"]
includes = []
for root, folder, files in os.walk("./safebox/src"):
    for file in files:
        if file.endswith("cpp"):
            sources.append(os.path.join(root, file))
    includes.append(root)

long_description = ""
with open("README.MD") as f:
    long_description = f.read()



extensions = [
    Extension(
        name="safebox",
        sources=sources,
        include_dirs=includes,
        define_macros=[
            ("PRIVATE_KEY", "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"),
            ("PRIVATE_IV", "bbbbbbbbbbbbbbbb")            
        ]
    )
]

setup(
    name="safebox",
    version=datetime.datetime.now().strftime("%Y%m%d%H%M%S"),
    description="A safe waay to store your Python application credetials",
    long_description=long_description,
    long_description_content_type='text/markdown',
    author="Mateus Michels de Oliveira",
    author_email="michels09@hotmail.com",
    ext_modules=cythonize(extensions),
    requires=["setuptools", "wheel", "Cython"],
    packages=find_packages(),
    url="https://github.com/MMichels/safebox"
)