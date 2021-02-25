from setuptools import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

setup(name="fps-limiter",
      version="0.1.1",
      description="Limit while loop at certain fps rate.",
      url="http://github.com/cartovarc/fps-limiter",
      author="Carlos Tovar",
      author_email="cartovarc@gmail.com",
      license="MIT",
      long_description=readme,
      packages=["fps_limiter"],
      zip_safe=False)
