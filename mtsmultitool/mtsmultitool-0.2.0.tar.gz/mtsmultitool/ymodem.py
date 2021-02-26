
import os
import binascii
import struct

import xmodem


class YMODEM:
    """
    YMODEM serial file transfer protocol.

    .. code-block:: python
        :caption: Send example

        def getc(size, timeout=1):
            return serial.read(size)

        def putc(data, timeout=1):
            return serial.write(data)

        xfer = YMODEM(getc, putc)
        if xfre.send('firmware.bin'):
            print('File sent successfully')
    """

    CRC_TIMEOUT = 5.0
    NAK_TIMEOUT = 10.0
    MAX_ERRORS = 10

    def __init__(self, getc, putc):
        self._getc = getc
        self._putc = putc
        self._x = xmodem.XMODEM(getc, putc, mode='xmodem1k')

    def send(self, file_path: str, setup_timeout: float = 10.0, callback: callable = None) -> bool:
        """
        Send a file.

        :param file_path: Path to file
        :param setup_timeout: Seconds to wait for the device to respond to setup packet
        :param callback: Reports status during transfer.  A called with `total_packets` = -1 after sending the initial
                         setup frame.
                         Expected signature: `def callback(total_packets, success_count, error_count)`
        :return: True if successful
        """
        file_size = os.path.getsize(file_path)
        file_name = os.path.basename(file_path).encode('utf-8')
        fc = 0  # Frame counter
        with open(file_path, 'rb') as fd:
            errors = 0
            while errors < YMODEM.MAX_ERRORS:
                c = self._getc(1, YMODEM.CRC_TIMEOUT)
                if c == xmodem.CRC:
                    # Pack file name and size into frame
                    frame = struct.pack(f'{len(file_name)}sB{len(str(file_size))}sc', file_name, 0x00, str(file_size).encode('utf-8'), b' ')
                    frame = frame.ljust(128, b'\x00')   # Pad out frame with 0's
                    crc = binascii.crc_hqx(frame, 0)    # Calculate CRC16 of frame
                    # Pack frame with header and CRC
                    packet = struct.pack(f'!cBB128sH', xmodem.SOH, (fc & 0xFF), (~fc & 0xFF), frame, crc)
                    self._putc(packet)
                    if callable(callback):
                        callback(-1,0,0)
                    c = self._getc(1, setup_timeout)
                    if c == xmodem.ACK:
                        errors = 0
                        break
                    else:
                        errors += 1

            if errors > 0:
                return False

            if not self._x.send(fd, callback=callback):
                return False

            self._putc(xmodem.EOT)
            c = self._getc(1, YMODEM.NAK_TIMEOUT)
            if c == xmodem.ACK:
                c = self._getc(1, YMODEM.NAK_TIMEOUT)

            if c == xmodem.CRC:
                frame = b'\x00' * 128
                crc = binascii.crc_hqx(frame, 0)  # Calculate CRC16 of frame
                # Pack frame with header and CRC
                packet = struct.pack(f'!cBB128sH', xmodem.SOH, (fc & 0xFF), (~fc & 0xFF), frame, crc)
                self._putc(packet)

                c = self._getc(1, YMODEM.NAK_TIMEOUT)

            return True
