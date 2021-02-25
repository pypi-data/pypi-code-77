# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hasspad', 'hasspad.handlers']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.4.1,<6.0.0',
 'RPi.GPIO>=0.7.0,<0.8.0',
 'click>=7.1.2,<8.0.0',
 'keybow>=0.0.3,<0.0.4',
 'pydantic>=1.7.3,<2.0.0',
 'rich>=9.8.2,<10.0.0',
 'spidev>=3.5,<4.0',
 'websockets>=8.1,<9.0']

entry_points = \
{'console_scripts': ['hasspad = hasspad.main:main']}

setup_kwargs = {
    'name': 'hasspad',
    'version': '0.1.1',
    'description': '',
    'long_description': '# hasspad\n\nA macropad interface for Home Assistant using the Pimoroni Keybow\n\n## Installation\n\nFirst, provision the device. Flash `raspios` and ensure `ssh` and WiFi access are enabled.\nThis can be done by writing a blank `ssh` file and a `wpa_supplicant.conf` file to the BOOT mount.\n\nOnce you are able to login to the device, perform some basic setup to set the hostname and enable SPI:\n\n```\nsudo raspi-config nonint do_hostname hasspad\nsudo raspi-config nonint do_spi 1\nsudo reboot\n```\n\nInstall `docker` and `docker-compose`:\n\n```\ncurl -sSL https://get.docker.com | sh\nsudo usermod -aG docker pi\n\nsudo apt-get install -y libffi-dev libssl-dev python3 python3-pip\nsudo pip3 install docker-compose\n```\n\nThe last thing you need to do is ensure environment variables are set that are used to authenticate with Home Assistant.\nYou can also pass these in as flags or modify `docker-compose.yml`:\n\n```\nexport HASSPAD_URI="ws://homeassistant.local:8123/api/websocket"\nexport HASSPAD_ACCESS_TOKEN="abcd"\n```\n\nFinally, just run `docker-compose up`.\n',
    'author': 'Kevin Chen',
    'author_email': 'keffcat@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/kvchen/hasspad/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
