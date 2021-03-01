from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

long_description = (here / "README.md").read_text(encoding="utf-8")

setup(
    name = "gitlist",
    version = "0.1.0", 
    description = "Displays the state of your local Git repositories.",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "https://github.com/craigiansmith/gitlist",
    author = "Craig Smith",
    author_email = "hello@craigiansmith.com.au",
    license = "GPLv3+",
    classifiers = [
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Version Control :: Git",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Programming Language :: Python :: 3.8",
    ],
    keywords = "git development source status",
    project_urls = {
        "Source": "https://github.com/craigiansmith/gitlist",
    },
    package_dir = {'':'src'},
    packages = find_packages(where='src', include=['gitlist', 'gitlist.*']),
    python_requires = ">=3.3",
    entry_points = {
        "console_scripts": [
            'gitlist=gitlist:main'
        ]
    }

)
