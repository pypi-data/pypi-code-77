from setuptools import find_packages, setup

setup(name='pycoloredprompt',
      version='1.0',
      description='Simple and lightweight cross-platform Python 16 colors terminal text package',
      author='Giovanni Sorgoni',
      author_email='g.sorgoni@icloud.com',
      license='MIT',
      packages=['pycolors'],
      url='https://github.com/gioggino/pycolors',
      project_urls={
          "GitHub Repo": "https://github.com/gioggino/pycolors",
          "Issues": "https://github.com/gioggino/pycolors/issues"
      },
      classifiers=[
          "Programming Language :: Python :: 2.7",
          "Programming Language :: Python :: 3",
          "Programming Language :: Python :: 3.9",
          "License :: OSI Approved :: MIT License",
          "Operating System :: OS Independent",
      ],
      zip_safe=False)
