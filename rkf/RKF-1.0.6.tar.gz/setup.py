from distutils.core import setup
from setuptools import setup

# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
  name = 'RKF',         # How you named your package folder (MyLib)
  long_description=long_description,
  long_description_content_type='text/markdown',
  packages = ['RKF'],   # Chose the same as "name"
  version = '1.0.6',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Implementation of Runge-Kutta Fehlberg method to numerically solve system of ODEs.',   # Give a short description about your library
  author = 'Amirhossein Rezaei',                   # Type in your name
  author_email = 'amirh.rezaei@mail.sbu.ac.ir',      # Type in your E-Mail
  url = 'https://github.com/amirh0ss3in/RKF',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/amirh0ss3in/RKF/archive/V_1.0.6.tar.gz',    # I explain this later on
  keywords = ['RKF', 'ODE', 'Runge-Kutta','Runge-Kutta Fehlberg'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'numpy','matplotlib'
      ],
  classifiers=[
    'Development Status :: 5 - Production/Stable',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Topic :: Scientific/Engineering',      # Define that your audience are developers
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
  ],
)
