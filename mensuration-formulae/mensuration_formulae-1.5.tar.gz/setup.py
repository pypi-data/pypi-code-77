from setuptools import setup

with open('README.md', 'r') as file:
     long_description = file.read()

setup(
    name='mensuration_formulae',
    version='1.5',
    description='A package that can calculate area,perimeter,surface areas and volumes of 2d & 3d geometric shapes. ',
    long_description=long_description,
    long_description_content_type='text/markdown',
    py_modules=['mensuration_formulae'],
    package_dir={'': 'src'},
    classifiers=[
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Operating System :: OS Independent",
    ],
    install_requires=[],
    url="https://github.com/venkat0701/mensuration_formulae",
    author='Venkateswar.S, Maria Irudaya Regilan J',
    author_email='s.venkateswar05@gmail.com'
)