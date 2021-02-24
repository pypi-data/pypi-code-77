from setuptools import setup 

with open ("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='helloworld_JeRaMeeee_2021',
    version='0.0.1',
    description='say hello!',
    py_modules=["helloworld"], 
    package_dir={'': 'src'},
    #classifiers=["Programming Language :: Python :: 3.6",],
    long_description=long_description, 
    long_description_content_type="text/markdown",
    #install_requires = [click,],
    #extras_require = {
    #    "dev": ["pytest=3.7"]
    #}
)

#### name is what peope pip install [name], no required to be file name
#### py_modules, list of modules, what it imports 
#### package dir, tells setup tools the code is in the 'src' directory 

#### build wheel, used to copy .py to build/lib/file_name.py, and its own ofiles 
#> python setup.py bdist_wheel 

#### install locally 
#> pip install -e . 

#### if using dev extras, others can install using > pip install -e .[dev]


######### setup notes for setup.py 
# python setup.py bdist_wheel sdist
# pip install twine 
# twine upload dist/* 
#
