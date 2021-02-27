from setuptools import setup, find_packages

requirements = []
with open('requirements.txt') as f:
    requirements = f.readlines()

setup(
    name='wave_api',
    version='0.1',
    description='API for Wave Google Sheets',
    author='jininvt',
    license='MIT',
    packages=find_packages(),
    install_requires=requirements,
)
