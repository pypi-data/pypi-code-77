from setuptools import setup


requires = []


setup(
    name='reprypt',
    version='2.0.2',
    description='Encryption Module',
    url='https://github.com/tasuren/reprypt',
    author='tasuren',
    author_email='tasuren5@gmail.com',
    license='MIT',
    keywords='encrypt decrypt',
    long_description=open("readme.md").read(),
    long_description_content_type="text/markdown",
    packages=[
        "reprypt"
    ],
    install_requires=requires,
    classifiers=[
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)