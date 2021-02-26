from setuptools import setup, find_packages

setup(name='pp-gameoflife',
	version='2.0',
	description='Custom game of life implementation',
	url='https://github.com/PhilippPilar/ASPP-project/GameOfLife',
	author='Philipp Pilar',
	author_email='philipp.pilar@it.uu.se',
	license='BSD',
	py_modules=['gameoflife','patterns'],
	packages=find_packages(exclude=['test']))
	#packages=['numpy','matplotlib','time'])