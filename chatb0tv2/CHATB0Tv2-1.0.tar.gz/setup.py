from setuptools import setup, find_packages

VERSION = '1.0'
DESCRIPTION = 'A Chatbot'
LONG_DESCRIPTION = """A easy to use chatbot package. Example: 
```py
from CHATB0Tv2 import Chatbot
while True:
    WhatYouWantToSay = input(">>> ")
    chatbot = Chatbot(WhatYouWantToSay)
    print(chatbot.response())

```
"""

# Setting up
setup(
    name="CHATB0Tv2",
    version=VERSION,
    author="myspacebarbroke",
    author_email="notmyrealemail@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['requests', 'CHATB0T100'],
    keywords=['chatbot'],
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
