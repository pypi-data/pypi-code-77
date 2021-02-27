import setuptools

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setuptools.setup(
    name="joke-api",
    version="1.0.0",
    author="proguy914629",
    description="A cool wrapper for Joke API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    install_requires=["requests"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    keywords=["joke", "jokes", "wrapper", "api"],
    entry_points={"console_scripts": ["quote=joke.cli:cli"]},
    python_requires=">=3.5",
    zip_safe=False
)