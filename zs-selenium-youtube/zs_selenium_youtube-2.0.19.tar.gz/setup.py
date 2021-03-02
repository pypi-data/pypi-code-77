import setuptools, os

readme_path = os.path.join(os.getcwd(), "README.md")
if os.path.exists(readme_path):
    with open(readme_path, "r") as f:
        long_description = f.read()
else:
    long_description = 'zs_selenium_youtube'

setuptools.setup(
    name="zs_selenium_youtube",
    version="2.0.19",
    author="Zselter",
    description="selenium_youtube",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Zselter07/selenium_youtube",
    packages=setuptools.find_packages(),
    install_requires=["kyoutubescraper", "selenium", "kstopit", "selenium_firefox", "kcu", "noraise", "selenium_uploader_account", "beautifulsoup4"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
)