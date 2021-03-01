from datetime import datetime, timedelta

from bhavpr.collection.constants import (
    PR_URL,
    PERIOD,
    PR_DIR_FORMAT,
    DATE_FORMAT_STR
)

def date_range_iter(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)

def preprocess_date(input_date):
    if isinstance(input_date, str):
        input_date = datetime.strptime(input_date, DATE_FORMAT_STR)
    return input_date

class PrProperties(object):
    def __init__(self, day, month, year) -> None:
        self.day = day
        self.month = month
        self.year = year

    @staticmethod
    def pad_zero(element, final_len=2):
        if element < 10:
            element = str(element).rjust(final_len, "0")
        return element

    @staticmethod
    def format_year(year):
        year = str(year)
        if len(year) > 2:
            year = year[-2:]
        return year

    @staticmethod
    def create_instance_from_directory(directory_name) -> object:
        dir_date = datetime.strptime(directory_name, PR_DIR_FORMAT)
        return PrProperties(dir_date.day, dir_date.month, dir_date.year)

    def get_file_name(self, directory=False) -> str:
        file_name = "PR{0}{1}{2}"

        day = PrProperties.pad_zero(self.day)
        month = PrProperties.pad_zero(self.month)
        year = PrProperties.format_year(self.year)

        file_name = file_name.format(day, month, year)
        if directory:
            return file_name
        file_name = "".join([file_name, ".zip"])
        return file_name

    def get_anddmmyy_file_name(self) -> str:
        file_name = self.get_file_name(directory=True)
        file_name = file_name.replace("PR", "an")
        return "".join([file_name, ".txt"])

    def get_bcddmmyy_file_name(self) -> str:
        file_name = self.get_file_name(directory=True)
        file_name = file_name.replace("PR", "bc")
        return "".join([file_name, ".csv"])

    def get_specific_file_name(self, prefix, extension) -> str:
        file_name = self.get_file_name(directory=True)
        file_name = file_name.replace("PR", prefix)
        return "".join([file_name, PERIOD, extension])

    def get_download_url(self) -> str:
        file_name = self.get_file_name()
        url = PR_URL.format(file_name)
        return url
