from pathlib import Path

from voicemailbox import logging


__version__ = '0.1.5'

# Activate logs
logger = logging.Logging().logger

# Define constants
STATIC_FILES_PATH = Path(__file__).parent / "static"
NEW_MAIL_SONG_PATH = STATIC_FILES_PATH / "songs" / "new_mail.mp3"
FONTAWESOME_PATH = (
        STATIC_FILES_PATH / "fonts" / "Font Awesome 5 Free-Solid-900.otf")
SLIDER_BORDER_PATH = STATIC_FILES_PATH / "images" / "blank_background.png"
SLIDER_CURSOR_PATH = STATIC_FILES_PATH / "images" / "circle-solid-24.png"
