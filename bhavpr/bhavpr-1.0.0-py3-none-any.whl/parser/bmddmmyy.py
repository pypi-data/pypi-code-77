import codecs
import os
from datetime import timedelta, date

from parser.company import Company
from collection.download_helper import PrProperties
from collection.constants import PR_DATA_DIR


class bmDDMMYY(Company):
    field_separator = " : "
    company_name_separator = "    "
    fields = ["company_name", "board_meeting_date", "puurpose"]

    def __init__(self, company_name, file_path):
        super().__init__(company_name)
        self.file_path = file_path
        self.process()
        hit = self.data.get(self.company_name, None)
        if hit:
            print(file_path)
            print(hit)

    def validation(self, record):
        if not record.get("company_name"):
            return False
        if len(record) < 3:
            return False
        company_names = record.get("company_name", "").split(
            bmDDMMYY.company_name_separator
        )
        if len(company_names) < 2:
            return False
        return True

    def process(self) -> None:
        """Processes the announcement file for a specific date. 
        Creates an index on the company symbol. 
        If a new line belongs to the company from previous line, 
        The line is taken as a new summary record and appended. 
        """
        self.data = {}
        prev_company = None
        with codecs.open(self.file_path, "r", encoding="latin") as file_handler:
            lines = file_handler.readlines()
            for line in lines:
                columns = [x.rstrip() for x in line.split(bmDDMMYY.field_separator)]
                element = dict(zip(bmDDMMYY.fields, columns))

                if not self.validation(element):
                    data_list = self.data.setdefault(prev_company, [])
                    data_list.append({"summary": line.rstrip()})
                    continue
                symbol = element["company_name"].split(bmDDMMYY.company_name_separator)[
                    1
                ]
                data_list = self.data.setdefault(symbol, [])
                data_list.append(element)

                prev_company = symbol


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
            file_path = os.path.join(
                directory_path,
                pr_props.get_specific_file_name(prefix="Bm", extension=".txt"),
            )
            instance = bmDDMMYY("ITC", file_path)
