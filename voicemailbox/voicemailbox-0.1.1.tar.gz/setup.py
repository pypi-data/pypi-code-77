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
    'version': '0.1.1',
    'description': 'Application for reading voice messages',
    'long_description': '# VoicemailBox\n\nVoicemailBox is an application for reading voice messages. Its graphical interface is based on the Kivy framework.\n\nCreated to run on a Raspberry Pi with a touch screen, it should work on any GNU/Linux system.\n\n## Installation - General case\n\nVoicemailBox can be installed with pip :\n```bash\npip install voicemailbox\n```\n\n## Installation - Raspberry Pi\n\nThe app has been tested on a Raspberry Pi 3, running Raspberry Pi OS Lite \n(Buster release), and the following hardware :\n- official Raspberry Pi touchscreen ;\n- OneNiceDesign touchscreen case ;  \n- adafruit speaker bonnet ;\n- adafruit stereo enclosed speaker set.\n\nOn this system, some packages have to be installed first \n([Source](https://kivy.org/doc/stable/installation/installation-rpi.html)) :\n```bash\napt install libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev \\ \nlibsdl2-ttf-dev pkg-config libgl1-mesa-dev libgles2-mesa-dev \\\npython3-setuptools libgstreamer1.0-dev \\\ngstreamer1.0-plugins-{bad,base,good,ugly} \\\ngstreamer1.0-{omx,alsa} python3-dev libmtdev-dev \\ \nxclip xsel libjpeg-dev gstreamer1.0-tools\n```\n\nThen, Kivy and VoicemailBox can be installed \n(virtual environment recommended) :\n```bash\npip install --upgrade pip setuptools Cython\npip install kivy[base,media] --no-binary kivy\npip install voicemailbox\n```\n\n### Additionnal configuration\n\n- create `ssh` file in `/boot` to enable ssh\n\n\n- edit  `/boot/config.txt` :\n\t- touchscreen rotation : add `lcd_rotate=2`\t\n\t- GPU\'s memory set to 256 Mb : add `gpu_mem=256`\n\t- adafruit speaker bonnet :\n\t\t- add `dtoverlay=hifiberry-dac`\n\t\t- add `dtoverlay=i2s-mmap`\n\t\t- comment `dtparam=audio=on`\n\t\n\n- for speaker bonnet support, create `/etc/asound.conf` with the following content :\n\t```text\n\tpcm.speakerbonnet {\n\t   type hw card 0\n\t}\n\n\tpcm.dmixer {\n\t   type dmix\n\t   ipc_key 1024\n\t   ipc_perm 0666\n\t   slave {\n\t     pcm "speakerbonnet"\n\t     period_time 0\n\t     period_size 1024\n\t     buffer_size 8192\n\t     rate 44100\n\t     channels 2\n\t   }\n\t}\n\n\tctl.dmixer {\n\t    type hw card 0\n\t}\n\n\tpcm.softvol {\n\t    type softvol\n\t    slave.pcm "dmixer"\n\t    control.name "PCM"\n\t    control.card 0\n\t}\n\n\tctl.softvol {\n\t    type hw card 0\n\t}\n\n\tpcm.!default {\n\t    type             plug\n\t    slave.pcm       "softvol"\n\t}\t   \n\t```\n\n\n- Wi-Fi : create wpa_supplicant.conf file in `/boot` with following content \n  ([Source](https://www.raspberrypi.org/documentation/configuration/wireless/headless.md)) :\n\t```text\n\tctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev\n\tupdate_config=1\n\tcountry=<Insert 2 letter ISO 3166-1 country code here>\n\t\n\tnetwork={\n\t ssid="<Name of your wireless LAN>"\n\t psk="<Password for your wireless LAN>"\n\t}\n\t```\n\n\n- to use kivy with Raspberry Pi touchscreen, modify `~/.kivy.config.ini`, \n  add under `[input]` section :\n\t```text\n\tmouse = mouse\n\tmtdev_%(name)s = probesysfs,provider=mtdev\n\thid_%(name)s = probesysfs,provider=hidinput\n\t```\n\n\n- add udev rule to use `rpi-backlight` without root access :\n\t```bash\n\t$ echo \'SUBSYSTEM=="backlight",RUN+="/bin/chmod 666 /sys/class/backlight/%k/brightness /sys/class/backlight/%k/bl_power"\' | sudo tee -a /etc/udev/rules.d/backlight-permissions.rules\n\t```\n\n\n- create systemd service : create `/etc/system/systemd/repondeur.service` \n  with the follonwing content :\n\t```text\n\t[Unit]\n\tDescription=repondeur\n\tAfter=multi-user.target\n\t\n\t[Service]\n\tType=idle\n\tEnvironment=KIVY_AUDIO=ffpyplayer\n\tExecStart=/home/pi/repondeur/env/bin/python -m repondeur\n\tWorkingDirectory=/home/pi/repondeur\n\tUser=pi\n\t\n\t[Install]\n\tWantedBy=multi-user.target\n\t```\n\n\n- use `ram2log` :\n\t- install :\n\t\t```bash\n\t\techo "deb http://packages.azlux.fr/debian/ buster main" | sudo tee /etc/apt/sources.list.d/azlux.list\n\t\twget -qO - https://azlux.fr/repo.gpg.key | sudo apt-key add -\n\t\tapt update\n\t\tapt install log2ram\n\t\t```\n\t- modify frequency : run `systemctl edit log2ram-daily.timer` and add :\n\t\t```text\n\t\t[Timer]\n\t\tOnCalendar=weekly\n\t\t```\n\n## License\n\nVoicemailBox is placed under \n[CeCILL license](http://cecill.info/licences/Licence_CeCILL_V2.1-en.html) \n(version 2.1).',
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
