import rpi_backlight
import tempfile
import pathlib


class Backlight(rpi_backlight.Backlight):
    """
    Wrapper for rpi_backlight.Backlight
    Mocks rpi_backlight.Backlight if run on unsupported platform
    """

    def __init__(self):

        self.fake_path = None

        try:
            super().__init__()
        except FileNotFoundError:

            self.temp_dir = tempfile.TemporaryDirectory()
            self.fake_path = pathlib.Path(self.temp_dir.name)

            files = {"bl_power": 0, "brightness": 255, "max_brightness": 255}

            for filename, value in files.items():
                (self.fake_path / filename).write_text(str(value))

            pathlib.Path(self.fake_path / "actual_brightness").symlink_to(
                self.fake_path / "brightness")

            super().__init__(backlight_sysfs_path=self.fake_path)
