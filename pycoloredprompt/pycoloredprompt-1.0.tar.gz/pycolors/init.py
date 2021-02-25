import os
import platform


def init():
    if platform.system() == 'Windows':  # Only if we are running on Windows
        os.system("")  # VT100 Emulation activation
