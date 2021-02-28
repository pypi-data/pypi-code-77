from setuptools import find_packages, setup

setup(
    name= "buildlytics",
    packages=['EDALIB'],
    version="0.0.3",
    platforms='any',
    description="A comprehensive way to make your Exploratory data analysis process easy by using our package",
    install_requires=[
          'numpy',
          'pandas',
          'seaborn'
      ],
    classifiers=[
        'Programming Language :: Python',
        'Operating System :: OS Independent',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering'
    ],
    license="MIT"
)
