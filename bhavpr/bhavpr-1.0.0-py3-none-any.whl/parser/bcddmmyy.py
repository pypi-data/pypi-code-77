import codecs
import csv
import os
from datetime import timedelta, date

from parser.company import Company
from collection.download_helper import PrProperties
from collection.constants import PR_DATA_DIR


class bcDDMMYY(Company):
    field_separator = " : "
    company_name_separator = "    "
    fields = [
        "series",
        "symbol",
        "security",
        "record_date",
        "book_closure_start_date",
        "bool_closure_end_date",
        "execution_date",
        "no_delivery_start_date",
        "no_delivery_end_date",
        "purpose",
    ]

    def __init__(self, company_name, file_path):
        super().__init__(company_name)
        self.file_path = file_path
        self.process()
        hit = self.data.get(self.company_name, None)
        if hit:
            print(file_path)
            print(hit)

    def validation(self, record):
        if not record.get("symbol"):
            return False
        return True

    def process(self) -> None:
        """Processes the corporate action details for securities 
        file for a specific date. 
        Creates an index on the company symbol. 
        """
        self.data = {}
        with codecs.open(self.file_path, "r", encoding="latin") as file_handler:
            reader = csv.reader(file_handler)
            for row in reader:
                element = dict(zip(bcDDMMYY.fields, row))
                if not self.validation(element):
                    continue
                symbol = element["symbol"]
                data_list = self.data.setdefault(symbol, [])
                data_list.append(element)


if __name__ == "__main__":
    t = date.today()
    start_date = t - timedelta(days=365)
    for offset in range(0, 365):
        cur_date = start_date + timedelta(days=offset)
        pr_props = PrProperties(
            day=cur_date.day, month=cur_date.month, year=cur_date.year
        )
        directory_name = pr_props.get_file_name(directory=True)
        directory_path = os.path.join(PR_DATA_DIR, directory_name)
        if os.path.isdir(directory_path):
            file_path = os.path.join(directory_path, pr_props.get_bcddmmyy_file_name())
            instance = bcDDMMYY("HAL", file_path)
