import os

from bhavpr.parser.anddmmyy import AnDDMMYY
from bhavpr.parser.company import Company
from bhavpr.collection.logger_factory import get_logger
from bhavpr.collection.download_helper import (
    PrProperties,
    preprocess_date,
    date_range_iter
)
from bhavpr.collection.constants import (
    PR_DATA_DIR,
    DEFAULT_COMPANY_NAME,
    ANNOUNCEMENT_PREFIX,
    TEXT_EXT,
    CSV_EXT,
)

class PRRecord(object):
    def __init__(self, pr_props, company_symbol=DEFAULT_COMPANY_NAME):
        dir_path = os.path.join(PR_DATA_DIR, pr_props.get_file_name(directory=True))
        self.announcements = AnDDMMYY(
            company_symbol,
            os.path.join(
                dir_path, pr_props.get_specific_file_name(ANNOUNCEMENT_PREFIX, TEXT_EXT)
            ),
        )

def load_meta(local=True) -> list:
    companies_set = set()
    for file_name in os.listdir(PR_DATA_DIR):
        abs_path = os.path.join(PR_DATA_DIR, file_name)
        if not os.path.isdir(abs_path):
            continue

        pr_props = PrProperties.create_instance_from_directory(file_name)
        pr_rec = PRRecord(pr_props)
        company_keys = pr_rec.announcements.data.keys()
        companies_set = companies_set.union(company_keys)
        if len(companies_set) > 4000:
            break
    return companies_set


def company_name_search(meta, pattern, only_name=False):
    return Company.company_name_search(meta, pattern, only_name)

def parse_pr_files(date_start, date_end, company_focus=None) -> dict:

    logger = get_logger(__name__)

    date_start = preprocess_date(date_start)
    date_end = preprocess_date(date_end)

    for cur_date in date_range_iter(date_start, date_end):
        pr_props = PrProperties(
            day=cur_date.day, month=cur_date.month, year=cur_date.year
        )
        try:
            pr_record = PRRecord(pr_props, company_symbol=company_focus)
        except FileNotFoundError as exc:
            logger.info("File not found for {}.".format(cur_date))
  
        
        
        
