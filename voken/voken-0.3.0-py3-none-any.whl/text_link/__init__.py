import os
import re
import pickle

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(BASE_DIR, 'text_link_pattern.pickle'), 'rb') as f:
    URL_PATTERN = pickle.load(f)

with open(os.path.join(BASE_DIR, 'hostname_pattern.pickle'), 'rb') as f:
    HOSTNAME_PATTERN = pickle.load(f)

TELEGRAM_USERNAME_PATTERN = re.compile(r'(?:t\.me|telegram\.me|0\.plus)/([a-zA-Z0-9][a-zA-Z0-9_]+[a-zA-Z0-9])')


def find_all_text_links(text):
    return re.findall(URL_PATTERN, text)


def get_hostname(text_link):
    matched = re.match(HOSTNAME_PATTERN, text_link)
    if matched:
        return text_link[matched.start():matched.end()]
    return


def get_telegram_username(text_link):
    matched = re.match(TELEGRAM_USERNAME_PATTERN, text_link)
    if matched:
        return matched.group(1)
    return
