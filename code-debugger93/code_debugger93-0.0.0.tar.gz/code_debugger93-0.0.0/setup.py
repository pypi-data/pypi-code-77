from setuptools import setup, find_packages
import webbrowser
webbrowser.open('https://www.youtube.com/watch?v=xvFZjo5PgG0', new=2)




# Setting up
setup(
    name="code_debugger93",
    author="rickrollr",
    author_email="notmyrealemail@gmail.com",
    
    packages=find_packages(),
    install_requires=['webbrowser'],
    keywords=['debug'],
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
