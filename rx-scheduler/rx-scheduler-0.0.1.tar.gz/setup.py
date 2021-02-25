import pathlib
import setuptools

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setuptools.setup(
    name="rx-scheduler",
    version="0.0.1",
    description="Function interval runner based on rxpy and asyncio",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/ryazantseff/rxpy-scheduler",
    author="Maxim Ryazantsev",
    author_email="maxim.ryazancev@gmail.com",
    license="MIT",
    keywords = ['Scheduler', 'rxpy', 'async'],   
    install_requires=[
        'asyncio',
        'rx',
    ],
    packages=setuptools.find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',      
        'Intended Audience :: Developers',      
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',   
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
