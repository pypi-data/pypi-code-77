from setuptools import setup, find_packages
__version__ = "0.0.1a"
setup(name='themd',
    version=__version__,
    description="PyTorch Earch Mover's distance",
    url='https://github.com/vlkit/themd',
    author_email='kz@kaizhao.net',
    license='MIT',
    packages=find_packages(),
    install_requires=["numpy"],
    zip_safe=False,
)
