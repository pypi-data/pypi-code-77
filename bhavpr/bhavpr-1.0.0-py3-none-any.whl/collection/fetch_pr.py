import os
import requests
import zipfile

from bhavpr.collection.download_helper import (
    PrProperties,
    preprocess_date,
    date_range_iter
)
from bhavpr.collection.logger_factory import get_logger
from bhavpr.collection.constants import PR_DATA_DIR

def download_data(date_start, date_end) -> None:

    logger = get_logger(__name__)

    date_start = preprocess_date(date_start)
    date_end = preprocess_date(date_end)

    for cur_date in date_range_iter(date_start, date_end):
        pr_props = PrProperties(
            day=cur_date.day, month=cur_date.month, year=cur_date.year
        )
        dir_path = os.path.join(PR_DATA_DIR, pr_props.get_file_name(directory=True))
        if os.path.isdir(dir_path):
            logger.info("Skipping to avoid repeat: {}".format(cur_date))
            continue
        url = pr_props.get_download_url()
        logger.info("URL to download: {}".format(url))
        result = requests.get(url)

        if result.status_code == 200:
            save_and_extract(result, pr_props)


def save_and_extract(response, pr_props) -> None:
    logger = get_logger(__name__)
    directory_name = pr_props.get_file_name(directory=True)
    directory_path = os.path.join(PR_DATA_DIR, directory_name)
    logger.debug("Directory path: {}".format(directory_path))
    if not os.path.isdir(directory_path):
        os.mkdir(directory_path)

    file_name = pr_props.get_file_name(directory=False)
    file_path = os.path.join(PR_DATA_DIR, file_name)
    file_handler = open(file_path, "wb")
    file_handler.write(response.content)
    file_handler.close()

    zipfile_handler = zipfile.ZipFile(file_path, "r")
    zipfile_handler.extractall(directory_path)


# load_meta()
