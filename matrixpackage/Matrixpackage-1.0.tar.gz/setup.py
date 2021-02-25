from setuptools import setup

##with open('README.md', 'r') as file:
    ##long_description = file.read()

setup(
    name='Matrixpackage',
    version='1.0',
    description='Matrix Package provides matrix addition,subtraction and matrix multiplication',
    ##long_description=long_description,
    ##long_description_content_type='text/markdown',
    py_modules=['Matrixpackage'],
    package_dir={'': 'src'},
    classifiers=[
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Operating System :: OS Independent",
    ],
    install_requires=[],
    url="https://github.com/pavishri/Velammal",
    author='Pavithra.K, Maria Irudaya Regilan J',
    author_email='<pavithrak.vec@gmail.com>'
)
