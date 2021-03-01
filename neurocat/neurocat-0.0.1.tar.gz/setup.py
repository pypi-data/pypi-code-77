import setuptools
import pathlib
import pkg_resources

with pathlib.Path('requirements.txt').open() as requirements_txt:
    install_requires = [
        str(requirement)
        for requirement
        in pkg_resources.parse_requirements(requirements_txt)
    ]


setuptools.setup(name='neurocat',
    version='0.0.1',
    author="Christoper Glenn Wulur",
    packages=[package for package in setuptools.find_packages() if package.startswith('neurocat')],
    zip_safe=False,
    author_email="christoper.glennwu@gmail.com",
    description="Interface Design for Neurocat's Research Engineer Test",
    install_requires=install_requires
)
