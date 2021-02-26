from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Beta',
    'Intended Audience :: Education, Developers',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='mcservstatus',
    version='0.0.2',
    description='Basic API wrapper for mcservstat.us. Docs are at https://mcservstatuspy.readthedocs.io/en/latest/? and may be incomplete.',
    long_description=open("README.md", "r").read(),
    url='https://github.com/xd-pro/mcservstatus',
    author='Finnbar M',
    author_email='xfinnbar@gmail.com',
    keywords='minecraft',
    packages=find_packages(),
    install_requires=['requests']
)
