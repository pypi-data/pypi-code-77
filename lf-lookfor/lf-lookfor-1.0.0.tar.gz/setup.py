from setuptools import setup, find_packages

setup(
    name='lf-lookfor',
    version='1.0.0',
    description='look for things',
    author='Taylor Gamache',
    author_email='gamache.taylor@gmail.com',
    url='https://github.com/breakthatbass/lookfor',
    packages=find_packages(),
    license='MIT',
    install_requires=['termcolor'],
    entry_points={
        'console_scripts' : ['lf = lookfor.lookfor:main']
   }
)
