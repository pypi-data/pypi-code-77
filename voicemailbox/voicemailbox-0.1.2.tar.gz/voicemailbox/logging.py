import logging.config
from pathlib import Path
import yaml


class Logging:

    def __init__(self):
        with open(Path(__file__).parent / "logging.conf", mode="r") as f:
            logging.config.dictConfig(yaml.load(f, Loader=yaml.FullLoader))
        self.logger = logging.getLogger("voicemailbox")
