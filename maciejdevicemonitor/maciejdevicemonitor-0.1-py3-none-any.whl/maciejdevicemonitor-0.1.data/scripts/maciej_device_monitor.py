"""
Devices monitor package written in Python. Before first use, please create directory for your devices.
Put one device per one file and make sure it's properly JSON formatted and it's .json file extension.
Example config (you can put more device features if there's need to):
{
  "voltage": 666,
  "current": 4
}
Results are written to stderr and log file.
Copyright (C) 2021 Maciej Czarkowski. All Rights Reserved.

To use, simply 'import maciej_device_monitor' and let it work!
To start monitor, use start(devices_directory, frequency) method with 2 parameters:
devices_directory - path to folder with your devices to monitor (string),
frequency - frequency of checking and logging devices state (seconds).
To stop device's monitor thread, use stop() method.
To get current devices statuses you can call get_statuses(devices_directory) method.
"""

import os
import json
from pathlib import Path
import threading
import time
import logging

# (https://youtrack.jetbrains.com/issue/PY-39762) Unhappy PyCharm issue
# noinspection PyArgumentList
logging.basicConfig(
    handlers=[logging.FileHandler("maciej_device_logs.log"), logging.StreamHandler()],
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

exitFlag = False


class DeviceMonitorThread(threading.Thread):
    def __init__(self, devices_directory, frequency):
        threading.Thread.__init__(self)
        self.devices_directory = devices_directory
        self.frequency = frequency

    def run(self):
        logging.info("Device monitor has started")
        while not exitFlag:
            get_statuses(self.devices_directory)
            time.sleep(self.frequency)


def start(devices_directory, frequency):
    """
        Start device monitor. Pass 'devices_directory' path to specify location of your devices config
        and 'frequency' to specify how often devices state should be logged (seconds).
    """
    global exitFlag
    exitFlag = False
    thread = DeviceMonitorThread(devices_directory, frequency)
    thread.name = "Device_monitor_thread"
    thread.start()


def stop():
    """
        Stop device monitor.
    """
    global exitFlag
    exitFlag = True
    logging.info("Device monitor has exited")


def get_statuses(devices_directory):
    """
        Get current devices statuses. Pass 'devices_directory' path to specify location of your devices config.
    """
    data_dict = {}
    try:
        files = os.listdir(devices_directory)
    except FileNotFoundError:
        logging.error(f"Cannot find passed directory {devices_directory}")
        return
    for filename in files:
        if filename.endswith(".json"):
            with open(devices_directory + '/' + filename) as json_file:
                try:
                    data_dict[Path(filename).stem] = json.load(json_file)
                except json.decoder.JSONDecodeError:
                    logging.error(f"Cannot parse {filename}. Check your syntax.")
                except:
                    logging.error(f"An error occurred while parsing {filename}")
        else:
            logging.error(f"Unsupported file extension for {filename}. Ensure to create .json file for the device.")
    logging.info(data_dict)
    return data_dict
