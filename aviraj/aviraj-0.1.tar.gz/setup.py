import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
     name='aviraj',  
     version='0.1',
     #scripts=['aviraj-reader/execute'] ,
     author="Akshay Katkar",
     author_email="akshukatkar@gmail.com",
     description="A Dependency injection check package",
     long_description=long_description,
   long_description_content_type="text/markdown",
     url="https://github.com/akshukatkar/dependecy",
     packages=setuptools.find_packages(),
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
 )