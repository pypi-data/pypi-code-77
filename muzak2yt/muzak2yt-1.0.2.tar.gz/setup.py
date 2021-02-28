import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="muzak2yt", # Replace with your own username
    version="1.0.2",
    author="Sakimotor",
    description="Upload your favorite music albums directly to YouTube !",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Sakimotor/muzak2yt",
    project_urls={
        "Bug Tracker": "https://github.com/Sakimotor/muzak2yt/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
)