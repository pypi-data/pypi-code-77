import setuptools



setuptools.setup(
    name='EasyPlotGUI',
    packages=setuptools.find_packages(),
    version='0.1.3',
    license='GNU',
    description='Python library that makes it easy to have a Qt GUI with a matplotlib widget made in QtDesigner implemented on a script.',
    author='Marcel Soubkovsky',                   # Type in your name
    author_email='marcelclemente.msc@gmail.com',      # Type in your E-Mail
    # Keywords that define your package best
    url='https://github.com/marcelrsoub/EasyPlotGUI',
    keywords=['Graphics', 'Charts', 'GUI'],
    install_requires=[
            "matplotlib>=3.1"
            "PyQt5>=5.13",
        ],
    python_requires=">=3.6",
    classifiers=[
        # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Education',      # Define that your audience are developers
        'Topic :: Scientific/Engineering :: Physics',
        # Again, pick a license
        'License :: OSI Approved :: GNU General Public License (GPL)',
        # Specify which pyhton versions that you want to support
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
