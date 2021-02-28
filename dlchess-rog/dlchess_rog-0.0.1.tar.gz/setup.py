from setuptools import setup 

classifiers = [
    'License :: OSI Approved :: MIT License'
]

setup(
    name='dlchess_rog',
    version='0.0.1',
    description = 'My chess bot modules',
    py_modules=["processor","generator","sample","base","oneplane","layers"],
    package_dir={'':'src'},
    license='MIT'
)