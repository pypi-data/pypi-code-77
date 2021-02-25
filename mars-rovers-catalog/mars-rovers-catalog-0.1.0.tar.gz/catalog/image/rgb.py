"""Mars Rover RGB image module."""

from pathlib import Path
from collections import UserDict

from PIL import Image

from requests import get

from ..misc import logger


log_rgb, debug_rgb = logger('RGB', info_stdout=True)


class RGB(UserDict):
    """RGB image object."""

    def __init__(self, args):
        super().__init__()

        name, imgs, channels, urls, nb, instr, dim, camera_vector, sol, attitude = args

        self.name = name
        self.instrument = instr.replace('_LEFT', '').replace('_RIGHT', '')

        self.nb_imgs = nb
        self.imgs = imgs.split(',')
        self.channels = channels.split(',')
        self.urls = urls.split(',')

        self.dim = tuple(map(int, dim[1:-1].split(',')))
        self.camera_vector = camera_vector
        self.sol = sol
        self.attitude = attitude

        for channel, url in zip(self.channels, self.urls):
            self[channel] = url

    def __str__(self):
        return self.name

    def __repr__(self):
        return (f'<{self.__class__.__name__}> '
                f'{self} | {self.instrument} | '
                f'{self.nb_imgs} images | Channels: {",".join(self.channels)}')

    def __getitem__(self, key):
        if key not in 'RGB':
            return self.data[key]

        if key in self:
            return Image.open(get(self.data[key], stream=True).raw).split()[0]

        # Empty blank image if missing
        return Image.new('L', self.dim)

    @property
    def is_complete(self):
        """Check if the RGB image is complete."""
        return 'R' in self and 'G' in self and 'B' in self

    def save(self, output_dir='RGB'):
        """Save RGB image.

        The images will be save as:

            `OUTPUT_DIR/INSTRUMENT/IMG.jpg`

        """
        if not self.is_complete:
            missing = ', '.join({'R', 'G', 'B'} - set(self.keys()))
            log_rgb.warning('Missing channel: `%s` in %s', missing, self.name)
            return None

        fname = (Path(output_dir) / self.instrument / self.name).with_suffix('.jpg')

        if fname.exists():
            log_rgb.debug('%s exists', fname.name)
            return fname

        fname.parent.mkdir(parents=True, exist_ok=True)

        rgb = Image.merge('RGB', (self['R'], self['G'], self['B']))
        rgb.save(fname)

        log_rgb.info('Created: %s', fname.name)
        return fname
