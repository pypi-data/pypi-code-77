#!/usr/bin/env python3
# -*- coding:utf-8; mode:python -*-
#
# Copyright 2020-2021 Pradyumna Paranjape
# This file is part of ppsi.
#
# ppsi is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# ppsi is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with ppsi.  If not, see <https://www.gnu.org/licenses/>.
#
'''
Load yaml configuration file(s), temp storage folder

Load {action: '--flag', ...} for all available menus
Determine a root directory for temporary storage and log files
'''


import os
import typing
import yaml
from .sway_api import sway_nag


def get_defaults() -> typing.Tuple[str, str]:
    '''
    Returns:
        swayroot: Confirmed existing Path for sway files
        config: dictionary of default config fetched from default locations

    get default values
    '''
    # Shipped defaults
    swayroot = os.path.join(os.path.dirname(__file__), 'config')
    config = os.path.join(swayroot, 'ppsi.yml')

    def_loc: typing.List[typing.Tuple[typing.Optional[str],
                                      typing.Tuple[str, ...]]] = [
        (os.environ.get('XDG_CONFIG_HOME', None), ('sway',)),  # Good practice
        (os.environ.get('HOME', None), ('.config', 'sway') ),  # The same thing
    ]
    for location in def_loc:
        if location[0] is not None:
            test_root = os.path.join(location[0], *location[1])
            if os.path.isdir(test_root):
                swayroot = test_root
                break

    # default config
    for location in def_loc:
        if location[0] is not None:
            test_conf = os.path.join(location[0],*location[1], 'ppsi.yml')
            if os.path.exists(test_conf):
                config = test_conf
                break
    return swayroot, config


def read_config(
        custom_conf: str = None,
        swayroot: str = None
) -> typing.Tuple[str, dict]:
    '''
    Read ppsi configuration from supplied yml file or default
    Define swayroot to store log files.

    Args:
        custom_conf: custom path of config file ppsi.yml
        swayroot: custom path of root directory to store sway data

    Returns:
        swayroot, config referenced by ``menu``
    '''
    # default locations
    defroot, defconfig = get_defaults()
    if swayroot is None:
        swayroot = defroot
    if custom_conf is None:
        root_path = os.path.join(swayroot,"ppsi.yml")
        if os.path.exists(root_path):
            custom_conf = root_path
    if custom_conf is None:
        custom_conf = defconfig
    with open(custom_conf, "r") as config_h:
        try:
            config = yaml.safe_load(config_h)
        except (FileNotFoundError, yaml.composer.ComposerError) as err:
            sway_nag(msg=str(err), error=True)
    return os.path.realpath(swayroot), config
