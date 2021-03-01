from setuptools import find_packages, setup

setup(
    name='pyeden',
    packages=find_packages(include=['pyeden'], exclude=['tests']),
    version='0.1.0',
    url='https://github.com/',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers'
    ],
    description='Library for downloading EDEN datasets',
    author='SFT Group',
    license='MIT',
    long_description='Library for downloading EDEN datasets',
    install_requires=[
          'requests',
          'numpy',
          'glob3',
          'tqdm',
          'opencv-python'
      ]
)