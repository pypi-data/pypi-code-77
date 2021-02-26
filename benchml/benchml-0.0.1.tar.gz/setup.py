import setuptools

def get_description():
    return "Benchmarking and pipelining for chemical machine learning"

def get_scripts():
    return [
        "./bin/bbatch",
        "./bin/binfo",
        "./bin/bmark",
        "./bin/bxyz",
        "./bin/bml",
        "./bin/bmeta"
    ]

if __name__ == "__main__":
    setuptools.setup(
        name="benchml",
        version="0.0.1",
        author="capoe",
        author_email="carl.poelking@floatlab.io",
        url="https://github.com/capoe/benchml",
        description="Chemical ML workbench",
        long_description=get_description(),
        packages=setuptools.find_packages(),
        scripts=get_scripts(),
        setup_requires=[],
        install_requires=["numpy", "scipy", "scikit-learn"],
        include_package_data=True,
        ext_modules=[],
        license="Apache License 2.0",
        classifiers=[
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Science/Research",
            "Topic :: Scientific/Engineering :: Physics",
            "Topic :: Scientific/Engineering :: Chemistry",
            "Topic :: Scientific/Engineering :: Artificial Intelligence"
        ],
        keywords="chemical machine learning pipelining benchmarking",
        python_requires=">=3.7",
    )

