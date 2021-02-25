import os

from setuptools import setup, find_packages
from setuptools_scm import get_version

__author__ = "Johannes Hörmann"
__copyright__ = "Copyright 2020, IMTEK Simulation, University of Freiburg"
__maintainer__ = "Johannes Hörmann"
__email__ = "johannes.hoermann@imtek.uni-freiburg.de"
__date__ = "Mar 18, 2020"

module_dir = os.path.dirname(os.path.abspath(__file__))
readme = open(os.path.join(module_dir, 'README.md')).read()
version = get_version(root='.', relative_to=__file__)


def local_scheme(version):
    """Skip the local version (eg. +xyz of 0.6.1.dev4+gdf99fe2)
    to be able to upload to Test PyPI"""
    return ""


url = 'https://github.com/jotelha/fwrlm'

if __name__ == "__main__":
    setup(
        author='Johannes Laurin Hörmann',
        author_email='johannes.hoermann@imtek.uni-freiburg.de',
        name='fwrlm',
        description='FireWorks RocketLauncher Manager',
        long_description=readme,
        long_description_content_type="text/markdown",
        url=url,
        use_scm_version={
            "root": '.',
            "relative_to": __file__,
            "write_to": os.path.join("fwrlm", "version.py"),
            "local_scheme": local_scheme},
        packages=find_packages(),
        include_package_data=True,
        python_requires='>=3.6.5',
        zip_safe=False,
        install_requires=[
            'ansible >= 2.9.1',  # TODO: the dependency on ansible is only due two 4 simple jinja filters for the render utility, that should be removed at some point
            'fireworks>=1.9.5',
            'jinja2>=2.10',
            'jinja2-time>=0.2.0',
            'monty>=4.0.2',
            'paramiko>=2.4.2',
            'python-daemon>=2.2.4',
            'pid>=3.0.0',
            'psutil>=5.6.1',
            'tabulate>=0.8.2',
        ],
        setup_requires=['setuptools_scm'],
        tests_require=['pytest'],
        entry_points={
            'console_scripts': [
                'fwrlm = fwrlm.cli.fwrlm_run:main',
                'render = fwrlm.cli.render_run:main',
            ]
        },
        download_url="{}/tarball/{}".format(url, version),
        license='MIT',
    )
