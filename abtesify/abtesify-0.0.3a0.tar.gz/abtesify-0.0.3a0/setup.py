import setuptools

setuptools.setup(
    name="abtesify",  # Replace with your own username
    version="0.0.3-a0",
    author="Fangnikoue Evarist",
    author_email="malevae@gmail.com",
    description="A python program to send notification about the project update and new release.",
    url="https://github.com/eirtscience/abtesify",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Operating System :: OS Independent",
    ],
    scripts=['src/bin/abtesify'],
    install_requires=[
        'slackclient',
        'yagmail',
        'pyaml'
    ],
    python_requires='>=3.5',
)
