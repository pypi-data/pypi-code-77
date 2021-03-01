from setuptools import setup


setup(
    name='pyasyncserver',
    zip_safe=True,
    version='0.1.5',
    description='Modular asynchronous application service',
    url='https://github.com/agratoth/pyasyncserver',
    maintainer='Anton Berdnikov',
    maintainer_email='agratoth@yandex.ru',
    packages=[
        'pyasyncserver',
        'pyasyncserver.core',
        'pyasyncserver.core.logger',
        'pyasyncserver.apps',
        'pyasyncserver.pipes'
    ],
    package_dir={'pyasyncserver': 'pyasyncserver'},
    install_requires=[
        'uvloop>=0.15.2',
        'aiohttp>=3.7.4',
        'py-message-prototypes>=0.2.1'
    ],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    python_requires='>=3.8',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
)
