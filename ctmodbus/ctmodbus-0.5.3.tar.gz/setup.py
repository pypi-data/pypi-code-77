# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['ctmodbus']

package_data = \
{'': ['*']}

install_requires = \
['ctui>=0.7.3,<0.8.0',
 'psutil>=5.8.0,<6.0.0',
 'pymodbus>=2.4.0,<3.0.0',
 'pyserial>=3.5,<4.0',
 'tabulate>=0.8.9,<0.9.0']

entry_points = \
{'console_scripts': ['ctmodbus = ctmodbus.commands:main']}

setup_kwargs = {
    'name': 'ctmodbus',
    'version': '0.5.3',
    'description': 'A highly flexible Modbus tool made for penetration testers',
    'long_description': '# Control Things Modbus\n\nThe goal of ctmodbus is to become the security professional\'s Swiss army knife\nfor interacting with Modbus devices.  Once completed, features will include\nsupport for:\n\n- RTU and ASCII versions of serial Modbus  (DONE)\n- TCP and UDP versions of TCP/IP Modbus  (DONE)\n- Client and server options  (DONE in lib, server IN PROGRESS)\n- All standard Modbus functions  (reads DONE, writes IN PROGRESS)\n- Arbitrary custom Modbus functions\n- Reading addresses specified in lists and ranges (DONE)\n- Interval based polling\n- Clone feature to quickly create base data for simulator\n- Proxy feature between two modbus endpoints\n- Export to cthistorian and database\n\n# Installation:\n\nAs long as you have git and Python 3.6 or later installed, all you should need to do is:\n\n```\npip3 install ctmodbus\n```\n\n## Examples of current user interface commands once you start ctmodbus:\n\n```\n> connect tcp:10.10.10.1                          # start a client session\n> connect rtu:/dev/serial                         # works with serial too\n> connect ascii:com2                              # and and windows\n> connect udp:10.10.10.1:10502                    # even udp with custom ports\n> read id                                         # read device identifiers\n> read discrete_inputs 1                          # read coils and registers\n> read coils 1,3,5,7                              # with comma separated values\n> read input_register 5,10-30,90-99               # and ranges\n> read holding_register 50 9                      # or start address and count\n> write coils 128 0                               # write single values\n> write coils 76 01101001                         # or multiple values\n> write holding_register 1000 14302 188 305       # registers support int\n```\n\n## Planned ui commands once complete:\n\n```\n> write holding_register 1000 "My name is Mud"    # and strings\n> write holding_register 1400 DEADBEEF            # or raw hex\n> poll holding_register 1-10,15-19 1              # poll registers every second\n> tags add input1 input_register 1                # define tag names\n> tags add config2 holding_register 50-69         # tags can define ranges\n> tags add config3 holding_register 70 20         # and work with start & count\n> read tags input1 config2 config3                # tags simplify reads & writes\n> tags group configs config1 config2 config3      # create tag groups\n> tags export saved.tags                          # export and share tags\n> tags import saved.tags                          # import other\'s tags\n> clone tcp:10.10.10.10 coils 1-100               # clone coils from a device\n> clone tcp:10.10.10.10 all 1-100                 # or all types of values\n> simulate tcp:127.0.0.1:10502                    # so you can later simulate\n> proxy tcp:10.10.10.1:10502 rtu:com4             # proxy requests to device\n> function 33 0000 DEADBEEF                       # send custom functions\n> function 8 [0000-FFFF] 0000                     # brackets for enumeration\n> function 8 [0000-00FF] (0000)5                  # parenths for random fuzzing\n> raw 1234 0001 06 01 0000 0010                   # or full raw modbus payloads\n> tunnel listen tcp::6666                         # setup modbus tunnel service\n> tunnel connect tcp:10.1.1.1:6666                # connect from another comp\n> tunnel send exfiltration.txt                    # send files through tunnel\n> tunnel shell                                    # or open a terminal session\n> historian tcp:10.1.1.1:9300                     # transactions to cthistorian\n```\n\n## This tool is built upon these to key library:\n\n- [Control Things User Interface](https://github.com/ControlThingsTools/ctui)\n- [PyModbus](https://github.com/bashwork/pymodbus)\n\n\n## Copyright 2020 Justin Searle\n\nThis program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.\n\nThis program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.\n\nYou should have received a copy of the GNU General Public License along with this program.  If not, see <http://www.gnu.org/licenses/>.\n',
    'author': 'Justin Searle',
    'author_email': 'justin@controlthings.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://www.controlthings.io',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
