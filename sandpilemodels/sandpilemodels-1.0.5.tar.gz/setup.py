
from setuptools import setup

# reading long description from file


# specify requirements of your package here
REQUIREMENTS = ['scipy', 'matplotlib', 'numpy']

# some more details
CLASSIFIERS = [
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'Topic :: Scientific/Engineering :: Physics',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 2.6',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    ]

keywords = ['sandpile', 'cellular automaton']

# calling the setup function
setup(name='sandpilemodels',
      version='1.0.5',
      description='A small package for simulating sandpile model',
      url='https://github.com/bhavishrg/sandpilemodels',
      author='Bhavish Raj Gopal',
      author_email='gbhavish@gmail.com',
      license='MIT',
      packages=['sandpilemodels'],
      classifiers=CLASSIFIERS,
      install_requires=REQUIREMENTS,
      entry_points={
                    "console_scripts": ["sandpile=sandpilemodels:main",]
      }
      )
