from setuptools import setup, find_packages

classifiers = [
    'License :: OSI Approved :: MIT License'
]

setup(
    name='dlchessrog',
    version='0.0.2',
    description = 'My chess bot modules',
    # py_modules=["processor","generator","sample","base","oneplane","layers"],
    # package_dir={'':'src'},
    packages = find_packages(),
    license='MIT'
)