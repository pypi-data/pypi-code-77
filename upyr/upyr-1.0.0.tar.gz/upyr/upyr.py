# https://github.com/wogscpar/upower-python/blob/master/upower_python/upower.py

import dbus

batteries = list()

UPOWER_NAME = "org.freedesktop.UPower"
UPOWER_PATH = "/org/freedesktop/UPower"

DBUS_PROPERTIES = "org.freedesktop.DBus.Properties"
bus = dbus.SystemBus()

upower_proxy = bus.get_object(UPOWER_NAME, UPOWER_PATH) 
upower_interface = dbus.Interface(upower_proxy, UPOWER_NAME)

devices = upower_interface.EnumerateDevices()

class Battery:
    title:str

    def __init__(self, title:str, iface):
        self.title = title
        self._iface = iface

    @property
    def powerlevel(self) -> float:
        return float(battery_proxy_interface.Get(UPOWER_NAME + ".Device", "Percentage"))/100

for battery in devices:
    # Check if device is battery?
    battery_proxy = bus.get_object(UPOWER_NAME, battery)
    battery_proxy_interface = dbus.Interface(battery_proxy, DBUS_PROPERTIES)

    batteries.append(Battery(battery.title(), battery_proxy_interface))