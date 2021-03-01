import os
from appdirs import AppDirs
from pathlib import Path

PR_URL = "https://www1.nseindia.com/archives/equities/bhavcopy/pr/{0}"
app_dirs = AppDirs("BhavPR", "jcopps", version="0.0.1")
PR_DATA_DIR = app_dirs.user_data_dir
PR_LOG_DIR = app_dirs.user_log_dir
print("PR log directory: {}".format(PR_LOG_DIR))
PR_LOG_FILE = os.path.join(PR_LOG_DIR, "bhav_pr.log")
Path(PR_DATA_DIR).mkdir(parents=True, exist_ok=True)
Path(PR_LOG_DIR).mkdir(parents=True, exist_ok=True)

DATE_FORMAT_STR = "%d-%m-%Y"
PR_DIR_FORMAT = "PR%d%m%y"  # Two digits year
PERIOD = "."
DEFAULT_COMPANY_NAME = None
ANNOUNCEMENT_PREFIX = "an"
TEXT_EXT = "txt"
CSV_EXT = "csv"
