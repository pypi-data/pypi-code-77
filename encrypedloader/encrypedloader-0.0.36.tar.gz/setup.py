from setuptools import setup, find_packages
from distutils.extension import Extension
try:
    from Cython.Build import cythonize, build_ext
except:
    build_ext = None

version = '0.0.36'

setup(name='encrypedloader',
      version=version,
      description="import encrypted python code",
      long_description="""\
 """,
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='encrypted python code',
      author='Alexander.Li',
      author_email='superpowerlee@gmail.com',
      url='https://github.com/ipconfiger',
      license='MIT',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=True,
      install_requires=[
          "click>=7.1.2",
          "salsa20>=0.3.0"
      ],
      #cmdclass={'build_ext': build_ext},
      #ext_modules=cythonize("encrypedloader/loader.pyx", language_level="3"),
      cmdclass={},
      ext_modules=[Extension('encrypedloader.loader', ['encrypedloader/loader.c'])],
      entry_points={
                'console_scripts': ['encpy=encrypedloader:main'],
            }
      )
