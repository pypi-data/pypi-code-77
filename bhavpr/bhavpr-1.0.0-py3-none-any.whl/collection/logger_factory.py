import logging
from logging.handlers import RotatingFileHandler
from bhavpr.collection.constants import PR_LOG_FILE

logging.basicConfig(
    handlers=[
        RotatingFileHandler(
            filename=PR_LOG_FILE, mode="w", maxBytes=512000, backupCount=4
        )
    ],
    level=logging.DEBUG,
    format="%(levelname)s %(asctime)s %(message)s",
    datefmt="%m/%d/%Y%I:%M:%S %p",
)


def get_logger(name="bhavpr"):
    logger = logging.getLogger(name)
    return logger
