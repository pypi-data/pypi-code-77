import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


def read_req(req_file):
    with open(req_file) as req:
        return [line.strip() for line in req.readlines() if line.strip() and not line.strip().startswith('#')]


requirements = read_req('requirements.txt')


setuptools.setup(
    name="kdb-vault-tools",
    version="0.1.6",
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=requirements,
    author="Max Nikitenko",
    author_email="moaddib666@gmail.com",
    description="Tools for kdb vault managing",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    url="https://github.com/moaddib666/kdb-vault-tools",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
