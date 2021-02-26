from setuptools import setup, find_packages

setup(
    name='traint',
    version='0.1.0',
    description='traint.ai cli python package',
    url='https://github.com/heureka-labs/traint',
    author='Heureka Labs',
    author_email='traint@heureka-labs.de',
    license='MIT',
    packages=find_packages(),
    install_requires=[
      'click==7.1.2',
      'pyfiglet==0.7',
      'requests==2.24.0',
      'requests_toolbelt',
      'tabulate'
    ],
    entry_points = {
      'console_scripts': [
        'traint = cli.cli:main'
      ]
    },
    classifiers=[
        'Intended Audience :: Developers',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python :: 3'
    ],
)
