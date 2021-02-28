# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['voicemailbox']

package_data = \
{'': ['*'],
 'voicemailbox': ['static/fonts/*', 'static/images/*', 'static/songs/*']}

install_requires = \
['IMAPClient>=2.2.0,<3.0.0',
 'PyYAML>=5.4.1,<6.0.0',
 'kivy>=2.0.0,<3.0.0',
 'python-dotenv>=0.15.0,<0.16.0',
 'rpi-backlight>=2.2.0,<3.0.0']

setup_kwargs = {
    'name': 'voicemailbox',
    'version': '0.1.2',
    'description': 'Application for reading voice messages',
    'long_description': '# VoicemailBox\n\nVoicemailBox is an application for reading voice messages left on a fixed \ntelephone line.\n\nIts graphical interface is based on the Kivy framework.\n\nCreated to run on a Raspberry Pi with a touch screen, \nit should work on any GNU/Linux system.\n\n# Purpose\n\nIn France, some operators offer, as an option, to send voice messages left \non a fixed line to a given email address.\n\nVoicemailBox retrieves the voicemail messages thus sent, signals their arrival \nand offers a graphical interface to read them.\n\nFor now, it is designed to work with the French operator Bouygues Telecom.\n\n## Installation - General case\n\nVoicemailBox can be installed with pip :\n```bash\npip install voicemailbox\n```\n\n## Installation - Raspberry Pi\n\nThe app has been tested on a Raspberry Pi 3, running Raspberry Pi OS Lite \n(Buster release), and the following hardware :\n- official Raspberry Pi touchscreen ;\n- OneNiceDesign touchscreen case ;  \n- adafruit speaker bonnet ;\n- adafruit stereo enclosed speaker set.\n\nOn this system, some packages have to be installed first \n([Source](https://kivy.org/doc/stable/installation/installation-rpi.html)) :\n```bash\napt install libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev \\ \nlibsdl2-ttf-dev pkg-config libgl1-mesa-dev libgles2-mesa-dev \\\npython3-setuptools python3-dev libmtdev-dev \\ \nxclip xsel libjpeg-dev ffmpeg\n```\n\nThen, Kivy and VoicemailBox can be installed \n(virtual environment recommended) :\n```bash\npip install --upgrade pip setuptools Cython\npip install kivy[base,media] --no-binary kivy\npip install voicemailbox\n```\n\nTo allow `rpi-backlight` to manage touchscreen backlight without root access,\na udev rule has to be created :\n```bash\n$ echo \'SUBSYSTEM=="backlight",RUN+="/bin/chmod 666 /sys/class/backlight/%k/brightness /sys/class/backlight/%k/bl_power"\' | sudo tee -a /etc/udev/rules.d/backlight-permissions.rules\n```\n\n### Additionnal configuration\n\nThe following instructions enable VoicemailBox to be integrated \nwith the hardware described above :\n\n\n- edit  `/boot/config.txt` :\n\t- touchscreen rotation : add `lcd_rotate=2`\t\n\t- GPU\'s memory set to 256 Mb : add `gpu_mem=256`\n\t- adafruit speaker bonnet :\n\t\t- add `dtoverlay=hifiberry-dac`\n\t\t- add `dtoverlay=i2s-mmap`\n\t\t- comment `dtparam=audio=on`\n\t\n\n- for speaker bonnet support, create `/etc/asound.conf` with the following content :\n\t```bash\n\tpcm.speakerbonnet {\n\t   type hw card 0\n\t}\n\n\tpcm.dmixer {\n\t   type dmix\n\t   ipc_key 1024\n\t   ipc_perm 0666\n\t   slave {\n\t     pcm "speakerbonnet"\n\t     period_time 0\n\t     period_size 1024\n\t     buffer_size 8192\n\t     rate 44100\n\t     channels 2\n\t   }\n\t}\n\n\tctl.dmixer {\n\t    type hw card 0\n\t}\n\n\tpcm.softvol {\n\t    type softvol\n\t    slave.pcm "dmixer"\n\t    control.name "PCM"\n\t    control.card 0\n\t}\n\n\tctl.softvol {\n\t    type hw card 0\n\t}\n\n\tpcm.!default {\n\t    type             plug\n\t    slave.pcm       "softvol"\n\t}\t   \n\t```\n\n\n- Wi-Fi : create wpa_supplicant.conf file in `/boot` with following content \n  ([Source](https://www.raspberrypi.org/documentation/configuration/wireless/headless.md)) :\n\t```bash\n\tctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev\n\tupdate_config=1\n\tcountry=<Insert 2 letter ISO 3166-1 country code here>\n\t\n\tnetwork={\n\t ssid="<Name of your wireless LAN>"\n\t psk="<Password for your wireless LAN>"\n\t}\n\t```\n\n\n- to use kivy with Raspberry Pi touchscreen, modify `~/.kivy/config.ini`, \n  add under `[input]` section :\n\t```bash\n\tmouse = mouse\n\tmtdev_%(name)s = probesysfs,provider=mtdev\n\thid_%(name)s = probesysfs,provider=hidinput\n\t```\n\n- create systemd service to run at startup :\n  \n\t- create `/etc/systemd/system/voicemailbox.service` \n\t  with the follonwing content :\n\t\t```bash\n\t\t[Unit]\n\t\tDescription=voicemailbox\n\t\tAfter=multi-user.target\n\t\t\n\t\t[Service]\n\t\tType=idle\n\t\tEnvironment=KIVY_AUDIO=ffpyplayer\n\t\tExecStart=/home/pi/.venv/bin/python -m voicemailbox\n\t\tWorkingDirectory=/home/pi/\n\t\tUser=pi\n\t\t\n\t\t[Install]\n\t\tWantedBy=multi-user.target\n\t\t```\n\t\n\t- run at start-up :\n\t  ```bash\n\t  sudo systemctl enable voicemailbox\n      ```\n\n- use [Log2Ram](https://github.com/azlux/log2ram) :\n\t- install :\n\t\t```bash\n\t\techo "deb http://packages.azlux.fr/debian/ buster main" | sudo tee /etc/apt/sources.list.d/azlux.list\n\t\twget -qO - https://azlux.fr/repo.gpg.key | sudo apt-key add -\n\t\tapt update\n\t\tapt install log2ram\n\t\t```\n\t- modify frequency : run `systemctl edit log2ram-daily.timer` and add :\n\t\t```bash\n\t\t[Timer]\n\t\tOnCalendar=weekly\n\t\t```\n\n## Usage\n\nSome environment variables have to be defined before running the application :\n```bash\nVOICEMAILBOX_IMAP_SERVER # IMAP server address\nVOICEMAILBOX_EMAIL_ADDRESS # User email address\nVOICEMAILBOX_EMAIL_PASSWORD # User password\n```\n\nThen VoicemailBox can be launched :\n```bash\npython -m voicemailbox\n```\n\n## Third party libraries and dependencies\n\nVoicemailBox makes use of the following third party projects :\n- [Kivy](https://kivy.org) (MIT license) ;\n- [IMAPClient](https://imapclient.readthedocs.io) (New BSD license) ;\n- [rpi_backlight](https://github.com/linusg/rpi-backlight) (MIT license) ;\n- [python_dotenv](https://saurabh-kumar.com/python-dotenv) (BSD license) ;\n- [PYYaml](https://pyyaml.org) (MIT license).\n\n\nVoicemailBox also includes :\n- the [FontAwesome](https://fontawesome.com/) icons (SIL Open Font License) ;\n- the ring song from \n  [LaSonotheque.org](https://lasonotheque.org/detail-0292-clochette-1.html)\n  (Free license).\n\n\n## License\n\nVoicemailBox is placed under \n[CeCILL license](http://cecill.info/licences/Licence_CeCILL_V2.1-en.html) \n(version 2.1).',
    'author': 'Pierre Gobin',
    'author_email': 'dev@pierregobin.fr',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
