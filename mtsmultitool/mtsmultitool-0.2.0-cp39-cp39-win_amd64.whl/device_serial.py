
import os
import enum
import serial
import re
from datetime import datetime
import time
import abc


import timeit
import contextlib

from . import ymodem
from .device_types import DeviceSeries, DeviceProperties


@contextlib.contextmanager
def elapsed_timer():
    start = timeit.default_timer()
    elapser = lambda: timeit.default_timer() - start
    yield lambda: elapser()
    end = timeit.default_timer()
    elapser = lambda: end-start


BL_PROMPT = b'bootloader :>'
NEWLINE = b'\r\n'


def read_until_prompt(serif, elapsed, timeout):
    found = False
    prompt = b''
    while elapsed() < timeout:
        resp = serif.read(1)
        if resp == b'':
            break
        prompt += resp
        if prompt.endswith(BL_PROMPT[4:]):
            found = True
            break
    return found


class DeviceCommandNotSupported(Exception):
    """Raised when a attempting to issue a command not supported by a device."""
    pass


class DeviceEvent(enum.Enum):
    MANUAL_RESET_REQUEST = 1
    """Device requires manual reset."""
    AUTOMATIC_RESET = 2
    """Device reset automatically."""
    BOOTLOADER_ACTIVE = 3
    """Entered bootloader."""
    APPLICATION_ACTIVE = 4
    """Entered application."""
    FILE_TRANSFER_SUCCESS = 5
    """File transfer completed successfully."""
    FILE_TRANSFER_FAIL = 6
    """File transfer failed."""
    FILE_TRANSFER_SETUP = 7
    """Setting up file transfer."""
    APPLYING_UPDATE = 8
    """Update is being applied."""


class SerialInterface(metaclass=abc.ABCMeta):
    """
    Abstract base class for serial interfaces.

    :param device_properties: Device properties based on the series
    :param port: Service device name, must be set by `open()` if `None`
    :param baudrate: Serial baud rate, defaults to 115200 if `None`
    :param echo: Device echos commands
    :param event_cb: Callback taking SerialInterface and DeviceEvent arguments to handle device events
    """
    def __init__(self, device_properties: DeviceProperties, port: str or None = None, baudrate: int or None = None, echo: bool = True, event_cb=None):
        self._dev_props = device_properties
        self._port = port
        self._baudrate = baudrate
        self._ser = None
        self._echo = echo
        self._event_cb = event_cb

    def __enter__(self):
        """
        Opens the serial connection.
        :return: self
        """
        self.open()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Closes the serial connection.
        :param exc_type:
        :param exc_value:
        :param traceback:
        :return: False
        """
        self.close()
        return False

    @property
    def device_properties(self) -> DeviceProperties:
        """Device properties defined by series."""
        return self._dev_props

    @property
    def echo(self):
        """
        Device echoes characters sent.

        :getter: Get state of device echo
        :setter: Set local state of device echo, no change is made to the device
        """
        return self._echo

    @echo.setter
    def echo(self, value: bool):
        self._echo = value
    
    def open(self, port=None, baudrate=None):
        """
        Open the serial connection.

        :param port: Service device name, uses value set during initialization if `None`
        :param baudrate: Serial baud rate, uses value set during initialization if `None`
        """
        if self._ser is None:
            if port is not None:
                self._port = port
            if self._port is None:
                raise RuntimeError('Serial device name not specified')
            if baudrate is not None:
                self._baudrate = baudrate
            if self._baudrate is None:
                self._baudrate = 115200

            self._ser = serial.Serial(self._port, baudrate=self._baudrate, bytesize=8,
                parity='N', stopbits=1, timeout=0.25, xonxoff=0, rtscts=1)

    def close(self):
        """Close the serial connection."""
        if self._ser is not None:
            self._ser.close()
            self._ser = None

    @abc.abstractmethod
    def enter_bootloader(self, timeout: float = 30):
        """
        Enter device bootloader.
        :param timeout: Seconds to wait for device to to enter bootloader, defaults to 30.
        """
        pass

    @abc.abstractmethod
    def complete_upgrade(self, timeout: float = 30) -> bool:
        """
        Wait for application to start.

        :param timeout: Seconds to wait for application
        :return: True if no errors are detected
        """
        pass

    def write(self, data: str or bytes, end: bool = True, echo: bool or None = None, timeout: float = None) -> int:
        """
        Write to serial port.

        :param data: Data to write, strings are converted using utf-8 encoding
        :param end: Send newline characters
        :param echo: Read back what was written, use value of echo property if `None`
        :param timeout: Number of seconds to wait for all data to be written
        :return: Number of bytes written
        """
        if type(data) is str:
            data_bytes = data.encode('utf-8')
        else:
            data_bytes = data

        if echo is None:
            echo = self._echo

        written = 0
        if timeout is not None:
            with elapsed_timer() as elapsed:
                while written < len(data_bytes) and elapsed() < timeout:
                    written += self._ser.write(data_bytes)
        else:
            written = self._ser.write(data_bytes)

        if end:
            written += self._ser.write(NEWLINE)
        if echo:
            self._ser.read(written)

        return written

    def read(self, n: int, timeout: float = None) -> bytes:
        """
        Read from serial port.

        :param n: Number of bytes to read
        :param timeout: Number of seconds to wait for all data to be read, a single read timeout is used if `None`
        :return: Bytes read
        """
        if timeout is not None:
            c = b''
            with elapsed_timer() as elapsed:
                while len(c) < n and elapsed() < timeout:
                    c += self._ser.read(n)
            return c
        else:
            return self._ser.read(n)

    def read_until(self, terminator: bytes, timeout: float = None):
        """
        Read from serial port until terminator is encountered

        :param terminator: Bytes are read until this is encountered
        :param timeout: Number of seconds to wait for terminator, a single read timeout is used if `None`
        :return: Bytes read
        """
        if timeout is not None:
            c = b''
            with elapsed_timer() as elapsed:
                while elapsed() < timeout:
                    c += self._ser.read_until(terminator)
                    if c.endswith(terminator):
                        break
            return c
        else:
            return self._ser.read_until(terminator)

    def notify(self, event: DeviceEvent):
        if self._event_cb is not None:
            self._event_cb(self, event)


class CommandInterface(SerialInterface):
    """
    Serial connection to a device over it's AT Command interface.

    :param dev_props: Device properties based on the series
    :param port: Service device name, must be set by `open()` if `None`
    :param baudrate: Serial baud rate, defaults to 115200 if `None`
    :param event_cb: Callback taking SerialInterface and DeviceEvent arguments to handle device events
    """
    def __init__(self, dev_props, port=None, baudrate=None, event_cb=None):
        super(CommandInterface, self).__init__(dev_props, port, baudrate, echo=True, event_cb=event_cb)

    def __enter__(self):
        """
        Opens the serial connection.
        :return: self
        """
        super(CommandInterface, self).__enter__()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Closes the serial connection.
        :param exc_type:
        :param exc_value:
        :param traceback:
        :return: False
        """
        super(CommandInterface, self).__exit__(exc_type, exc_value, traceback)
        return False

    def open(self, port=None, baudrate=None):
        """
        Open the serial connection.
        :param port: Service device name, uses value set during initialization if `None`
        :param baudrate: Serial baud rate, uses value set during initialization if `None`
        :return:
        """
        super(CommandInterface, self).open(port, baudrate)

    def enter_bootloader(self, timeout: float = 30):
        """
        Enter bootloader.  The AT interface uses the ATZ command to reset the device.  If the device receives
        'mts' within 250ms of booting it will stay in the bootloader.

        :param timeout: Seconds to wait for device to to enter bootloader, defaults to 30.
        """
        # Issue reset command
        self._ser.write(b'ATZ')
        self._ser.write(NEWLINE)

        # AT interface requires 'mts' to enter bootloader
        with elapsed_timer() as elapsed:
            while elapsed() < timeout:
                self._ser.write(b'm')
                resp = self.read(1)
                if resp == b'm':
                    self._ser.write(b'ts\r\n')
                    resp = self.read(1)
                    if resp == b't':
                        if read_until_prompt(self, elapsed, timeout):
                            break
            # Timed out
            if elapsed() > timeout:
                raise TimeoutError

        # Read any remaining bytes
        while len(self._ser.read(100)) > 0:
            pass

        self.notify(DeviceEvent.BOOTLOADER_ACTIVE)

    def complete_upgrade(self, timeout: float = 30) -> bool:
        """
        Wait for application to start.  The command interface sends no indication when upgrade is done.

        :param timeout: Seconds to wait for application
        :return: True
        """
        time.sleep(timeout)
        return True


class DebugInterface(SerialInterface):
    """
    Serial connection to a device over it's Debug interface.

    :param dev_props: Device properties based on the series
    :param port: Service device name, must be set by `open()` if `None`
    :param baudrate: Serial baud rate, defaults to 115200 if `None`
    :param event_cb: Callback taking SerialInterface and DeviceEvent arguments to handle device events
    """
    def __init__(self, dev_props: DeviceProperties, port: str or None = None, baudrate: int or None = None, event_cb=None):
        super(DebugInterface, self).__init__(dev_props, port, baudrate, echo=False, event_cb=event_cb)

    def __enter__(self):
        """
        Opens the serial connection.
        :return: self
        """
        super(DebugInterface, self).__enter__()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Closes the serial connection.
        :param exc_type:
        :param exc_value:
        :param traceback:
        :return: False
        """
        super(DebugInterface, self).__exit__(exc_type, exc_value, traceback)
        return False

    def open(self, port: str or None = None, baudrate: int or None = None):
        """
        Open the serial connection.
        :param port: Service device name, uses value set during initialization if `None`
        :param baudrate: Serial baud rate, uses value set during initialization if `None`
        """
        super(DebugInterface, self).open(port, baudrate)

    def enter_bootloader(self, timeout: float = 30):
        """
        Enter bootloader.  The debug interface requires a user to manually reset the device.  If the device receives
        input within 250ms of booting it will stay in the bootloader.

        :param timeout: Seconds to wait for device to to enter bootloader, defaults to 30.
        """
        # Debug interface requires a keypress to enter bootloader, but the
        # device must be reset manually
        self.notify(DeviceEvent.MANUAL_RESET_REQUEST)
        with elapsed_timer() as elapsed:
            while elapsed() < timeout:
                self.write(NEWLINE)
                if read_until_prompt(self, elapsed, 3):
                    break
            # Timed out
            if elapsed() > timeout:
                raise TimeoutError

        # Read any remaining bytes
        while len(self.read(100)) > 0:
            pass
        self.notify(DeviceEvent.BOOTLOADER_ACTIVE)

    def complete_upgrade(self, timeout: float = 30) -> bool:
        """
        Complete upgrade and wait for application to start.

        :param timeout: Seconds to wait for application
        :return: True if successful
        """
        output = b''
        status = False
        with elapsed_timer() as elapsed:
            while elapsed() < timeout:
                q = self.read(1024)
                output += q
                m = re.findall(b'(successful|Failed)', output)
                if len(m) == 1:
                    if m[0] == b'successful':
                        status = True
                    break
        return status


class DeviceBootloader:
    """
    Interact with device bootloader over a serial interface.  When used as a context manager the device bootloader is
    entered and exited automatically.

    .. code-block:: python
        :caption: Context usage example

         def progress(transferred, total, msg):
            if msg is not None:
                print('\r  {msg}', flush=True, end='')
            else:
                if transferred > total:     # Padding bytes can be included in the transferred amount
                    transferred = total
                p = transferred / total
                print('\r  ' + f'{p:.1%}'.rjust(6, ' ') + f' -- {int(transferred / 1024)} of {int(total / 1024)} KB',
                      flush=True, end='')

         def device_event_handler(serif, evt):
            if evt == device_serial.DeviceEvent.MANUAL_RESET_REQUEST:
                print("Reset device now")
            elif evt == device_serial.DeviceEvent.AUTOMATIC_RESET:
                print("Device reset")
            elif evt == device_serial.DeviceEvent.BOOTLOADER_ACTIVE:
                print("Successfully entered bootloader")

        try:
            with device_serial.CommandInterface(dp, args.port, args.baudrate, event_cb=device_event_handler) as serif:
                try:
                    with device_serial.DeviceBootloader(serif) as bl:
                        print("Transferring upgrade file...")
                        if bl.send_upgrade(output_file, apply=False, progress=progress):
                            print()
                            print('  Transfer completed successfully')
                            print('Applying upgrade...')
                            if bl.flash():
                                print(f'  {dp.name} upgraded')
                            else:
                                print('  Upgrade failed')
                        else:
                            print()
                            print('  Transfer failed')
                except TimeoutError:
                    print('Timeout when entering bootloader')
        except:
            print("Failed to open serial port")

    :param device_properties: Device properties based on the series
    :param port: Service device name, must be set by `open()` if `None`
    :param baudrate: Serial baud rate, defaults to 115200 if `None`
    :param echo: Device echos commands
    :param event_cb: Callback taking SerialInterface and DeviceEvent arguments to handle device events
    """
    def __init__(self, serial_interface: SerialInterface):
        self._serif = serial_interface
        self._echo_app = self._serif.echo
        self._serif.echo = True
        self._progress_callback = None

    def __enter__(self):
        """Enter the device bootloader"""
        self._serif.enter_bootloader()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Boot the application"""
        self.boot()
        return False

    def _enter_application(self):
        self._serif.echo = self._echo_app

    def _write_cmd(self, cmd: str or bytes):
        self._serif.write(cmd, end=True)
        resp = self._serif.read_until(BL_PROMPT)
        return resp[:-1 * len(BL_PROMPT)].decode('utf-8')

    def _progress(self, size: int, msg=None):
        if self._progress_callback is not None:
            self._xferd += size
            self._progress_callback(self._xferd, self._xfer_size, msg)

    def _send_file(self, cmd: str or bytes, src_name: str, dst_name: str or None = None) -> bool:
        if cmd == 'recv':
            if dst_name is None:
                dst_name = os.path.basename(src_name)

            if self._serif.device_properties.bootloader_transfer_simple:
                cmd = f'{cmd} ymodem {dst_name}'
            else:
                cmd = f'{cmd} {dst_name}'
        else:
            if self._serif.device_properties.bootloader_transfer_simple:
                cmd = f'{cmd} ymodem'
            else:
                cmd = f'{cmd}'

        self._serif.write(cmd)
        with elapsed_timer() as elapsed:
            while elapsed() < 30:
                resp = self._serif.read(1)
                if resp == b'C':
                    break
            if elapsed() >= 30:
                raise TimeoutError

        self._xfer_size = os.path.getsize(src_name)
        self._xferd = 0

        def _getc(size, timeout=1):
            return self._serif.read(size, timeout=timeout)

        def _putc(data, timeout=1):
            return self._serif.write(data, end=False, echo=False, timeout=timeout)

        def _status(total_packets, success_count, error_count):
            if total_packets == -1:
                self._serif.notify(DeviceEvent.FILE_TRANSFER_SETUP)
            else:
                self._progress(1024)

        modem = ymodem.YMODEM(_getc, _putc)
        return modem.send(src_name, self._serif.device_properties.transfer_setup_time, _status)

    def reset(self):
        """Reset the device."""
        self._serif.write('reset')
        self._enter_application()

    def boot(self):
        """Boot the device application."""
        self._serif.write('boot')
        self._enter_application()

    def erase(self):
        """Boot the device application."""
        self._serif.write('erase')

    def send_file(self, src_name: str, dst_name: str or None = None, progress: callable((int, int)) = None) -> bool:
        """
        Send a file to the device.

        :param src_name: Path to file to send
        :param dst_name: Name of file saved to the device
        :param progress: Callback for progress updates
        :return: True if the file transfer is successful
        """
        self._progress_callback = progress
        self._send_file('recv', src_name, dst_name)
        resp = self._serif.read_until(BL_PROMPT)
        resp = resp[:-1 * len(BL_PROMPT)]
        result = resp.find(b'ERROR') == -1
        self._serif.notify(DeviceEvent.FILE_TRANSFER_SUCCESS if result else DeviceEvent.FILE_TRANSFER_FAIL)
        self._progress_callback = None
        return result

    def send_upgrade(self, src_name: str, apply: bool = True, progress: callable((int, int)) = None) -> bool:
        """
        Send a file to the device as a firmware upgrade.  When sending to an xDot the Upgrade is always applied
        immediately after transferring.

        :param src_name: Path to file to send
        :param apply: Upgrade is applied immediately after transferring if True
        :param progress: Callback for progress updates
        :return: True if successful
        """
        self._progress_callback = progress
        if apply or self._serif.device_properties.series == DeviceSeries.XDOT.name:
            result = self._send_file('upgrade', src_name)
            self._serif.notify(DeviceEvent.FILE_TRANSFER_SUCCESS if result else DeviceEvent.FILE_TRANSFER_FAIL)
            if result:
                self._serif.notify(DeviceEvent.APPLYING_UPDATE)
                result = self._serif.complete_upgrade(self._serif.device_properties.upgrade_time)
            else:
                self.boot()
            self._serif.notify(DeviceEvent.APPLICATION_ACTIVE)
        else:
            result = self._send_file('transfer', src_name)
            if result:
                resp = self._serif.read_until(BL_PROMPT)
                result = resp.find(b'ERROR') == -1

            self._serif.notify(DeviceEvent.FILE_TRANSFER_SUCCESS if result else DeviceEvent.FILE_TRANSFER_FAIL)

        self._progress_callback = None
        return result

    def list_files(self) -> list:
        """
        Get a list of files present on the device.  Only supported on xDot when external flash is available.

        :return: List of file names and sizes
        """
        resp = self._write_cmd(f'list')
        files = list()
        if resp.find('ERROR') == -1:
            for line in resp.splitlines()[1:]:
                parts = line.split()
                if len(parts) == 2:
                    files.append((parts[1], int(parts[0])))
        return files

    def delete_file(self, file_name: str) -> bool:
        """
        Delete a file from the device.  Only supported on xDot when external flash is available.

        :param file_name: Name of file to delete
        :return: True if successful
        """
        resp = self._write_cmd(f'delete {file_name}')
        return resp.find('ERROR') == -1

    def flash(self):
        """
        Apply an upgrade that was previously transferred.  Not supported by xDot.
        :return: True if successful
        """
        if self._serif.device_properties.series == DeviceSeries.XDOT.name:
            raise DeviceCommandNotSupported

        self._write_cmd('flash')
        self._serif.notify(DeviceEvent.APPLYING_UPDATE)
        return self._serif.complete_upgrade(self._serif.device_properties.upgrade_time)
