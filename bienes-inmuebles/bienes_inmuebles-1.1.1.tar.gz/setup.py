import setuptools


setuptools.setup(name='bienes_inmuebles',
      version="1.1.1",
      url = "https://github.com/alexxfernandez13/bienes_inmuebles",
      description='Tool for predicitng real estate prices',
      author='Alejandro Fernandez y Paco Leon',
      author_email='alexxfernandez@hotmail.es',
      packages=setuptools.find_packages(),
      install_requires=["numpy", "matplotlib==3.2", "scipy", "pandas", "scikit-learn", "sklearn", "pytest", "joblib", "colorama"],
      classifiers=[
       "Programming Language :: Python :: 3",
       "License :: OSI Approved :: MIT License",
       "Operating System :: OS Independent",
       ],
     )