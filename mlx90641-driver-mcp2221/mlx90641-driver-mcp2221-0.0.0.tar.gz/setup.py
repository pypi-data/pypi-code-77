from setuptools import setup

version = '0.0.0'

requires = ['mlx90641-driver>=0.1.0']

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='mlx90641-driver-mcp2221',
    version=version,
    description='I2C for MLX90641 using MCP2221 USB to I2C adaptor',
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='Apache License, Version 2.0',
    # entry_points = {'console_scripts': ['mlx90641-dump-frame = mlx.examples.mlx90640_dump_frame:main']},
    entry_points={'console_scripts': []},
    install_requires=requires,
    url='https://github.com/melexis-fir/mlx90641-driver-mcp2221-py',
    # Provide either the link to your github or to your website
    download_url='https://github.com/melexis-fir/mlx90641-driver-mcp2221-py/archive/V' + version + '.tar.gz',
    packages=['mlx90641_driver_mcp2221'],
    package_dir={'mlx90641_driver_mcp2221': 'mcp2221'},
    package_data={'mlx90641_driver_mcp2221': ['libs/**/*.dll', 'libs/**/*.so']},

    classifiers=[
        # complete classifier list: http://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 3',
        'Topic :: Utilities',
    ],
)
