from bhavpr.collection.logger_factory import get_logger
from bhavpr.collection.fetch_pr import download_data
from bhavpr.parser.pr_record import parse_pr_files, load_meta, company_name_search


class BhavPR(object):
    def __init__(self):
        self.logger = get_logger()
        self.meta = load_meta(local=True)
        self.focus = None
        pass

    def collect(self, date_start, date_end) -> bool:
        """Downloads and extracts PR zip files to a temporary directory.
        date_start: Format as 01-01-2020 DD-MM-YYYY
        date_end: Format as 05-01-2020 DD-MM-YYYY
        """
        self.logger.info(
            "collect(): Received inputs {}, {}".format(date_start, date_end)
        )
        download_data(date_start, date_end)
        self.meta = load_meta(local=True)
        return True

    def get_symbol(self, search_string, only_name=False) -> set:
        return company_name_search(self.meta, search_string, only_name)

    def set_company(self, company_name) -> bool:
        record = self.get_symbol(company_name, only_name=True)
        if len(record) != 1:
            return False
        self.focus = record.pop()
        return True

    def get_pr(self, date_start, date_end) -> dict:
        """Returns a dictionary
        Indexed on date.
        Filtered by company if a symbol loaded.
        """
        return parse_pr_files(date_start, date_end, self.focus)
        
