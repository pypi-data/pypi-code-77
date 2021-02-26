
import enum


class DeviceSeries(enum.Enum):
    """Supported device series names."""
    MTDOT = 1
    """mDot"""
    MDOT = 1
    """mDot"""
    XDOT = 2
    """xDot"""
    MTQ = 3
    """Dragonfly"""
    MTQN = 4
    """Dragonfly Nano"""


class DeviceProperties:
    """Defines device properties based on the series."""
    def __init__(self, series: DeviceSeries):
        """
        Initialize properties.
        :param series: Device series
        """
        self._series = series

    @property
    def series(self) -> str:
        """Device series name."""
        return self._series.name

    @property
    def app_offset(self) -> int:
        """Offset in bytes from start of flash that the application is written."""
        if self._series == DeviceSeries.XDOT:
            return 0x0D000
        else:
            return 0x10000

    @property
    def target_name(self):
        """Target name used by mbed."""
        if self._series == DeviceSeries.MDOT:
            return "MTS_MDOT_F411RE"
        elif self._series == DeviceSeries.XDOT:
            return "XDOT_L151CC"
        elif self._series == DeviceSeries.MTQ:
            return "MTS_DRAGONFLY_F411RE"
        elif self._series == DeviceSeries.MTQN:
            return "MTS_DRAGONFLY_L471QG"

    @property
    def name(self):
        """Friendly name."""
        if self._series == DeviceSeries.MDOT:
            return "mDot"
        elif self._series == DeviceSeries.XDOT:
            return "xDot"
        elif self._series == DeviceSeries.MTQ:
            return "Dragonfly"
        elif self._series == DeviceSeries.MTQN:
            return "Dragonfly Nano"

    @property
    def bootloader_verbose(self):
        """Bootloader uses verbose output."""
        if self._series == DeviceSeries.XDOT:
            return False
        else:
            return True

    @property
    def bootloader_transfer_simple(self):
        """Bootloader supports simple transfers."""
        if self._series == DeviceSeries.XDOT:
            return False
        else:
            return True

    @property
    def bootloader_commands(self) -> list:
        """List of commands accepted by the device's bootloader."""
        cmd_set = ['boot', 'upgrade', 'send', 'reset', 'delete', 'list', 'erase', 'recv', 'flash', 'transfer', 'help']
        if self._series == DeviceSeries.XDOT:
            cmd_set = cmd_set[:7]
        return cmd_set

    @property
    def transfer_setup_time(self) -> float:
        """Number of seconds to allow for the device to setup a file transfer."""
        if self._series == DeviceSeries.XDOT:
            return 30.0
        return 15.0

    @property
    def upgrade_time(self) -> float:
        """Number of seconds to allow for the device to perform an upgrade."""
        if self._series == DeviceSeries.XDOT:
            return 240.0
        return 30.0
