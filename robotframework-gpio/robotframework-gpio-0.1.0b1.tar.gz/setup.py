# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['GPIOLibrary',
 'GPIOLibrary.keywords',
 'GPIOLibrary.mocks',
 'GPIOLibrary.mocks.RPi',
 'utests']

package_data = \
{'': ['*']}

install_requires = \
['robotframework>=3.2.2,<4.0.0']

setup_kwargs = {
    'name': 'robotframework-gpio',
    'version': '0.1.0b1',
    'description': "Robot Framework Library for interfacing GPIO pins on executing robot files on Raspberry Pi's. ",
    'long_description': '# GPIOLibrary\n\n![pypi-badge](https://img.shields.io/pypi/v/robotframework-gpio)\n![build-badge](https://api.travis-ci.com/ycbayrak/robotframework-gpio.svg)\n![unstable](https://img.shields.io/static/v1?label=status&message=unstable&color=red)\n\n\nRobot Framework Library for interfacing GPIO pins on executing robot files on Raspberry Pi\'s.\n\n## Requirements\n\n- [Robot Framework (^3.2.2) ](https://pypi.org/project/robotframework/)\n- [RPi.GPIO (^0.7.0)](https://pypi.org/project/RPi.GPIO/)\n\n## Installation\n\nInstall [RPi.GPIO](https://pypi.org/project/RPi.GPIO/) with command below;\n\n```\npip install RPi.GPIO\n```\n\nThen install GPIOLibrary with;\n\n```shell\npip install robotframework-gpio\n```\n\n\n## Example\n\n```robot\n*** Settings ***\n\nDocumentation   Test LED is fully functional\n\nLibrary                     Dialogs\nLibrary                     GPIOLibrary\n\nSuite Setup                 Begin GPIO Test\n\n*** Variables ***\n\n${LED_PIN}                  17\n\n*** Test Cases ***\n\nLED Should On\n    Set Output Pin          ${LED_PIN}\n    Set Pin High            ${LED_PIN}\n    Execute Manual Step     "Is LED On?"\n\nLED Should Off\n    Set Output Pin          ${LED_PIN}\n    Set Pin Low             ${LED_PIN}\n    Execute Manual Step     "Is LED Off?"\n    \n \n*** Keywords ***\n\nBegin GPIO Test\n    Set Mode                BOARD\n    Set Warnings Off\n```\n\n',
    'author': 'Yusuf Can Bayrak',
    'author_email': 'yusufcanbayrak@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
