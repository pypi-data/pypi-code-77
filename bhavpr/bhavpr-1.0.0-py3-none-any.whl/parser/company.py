import re


class Company(object):
    def __init__(self, company_name, symbol=""):
        self.company_name = company_name
        self.symbol = symbol
        if isinstance(company_name, list):
            self.company_name = company_name[0]
            self.symbol = companny_name[1]

    def __eq__(self, other):
        return self.company_name == other.company_name and self.symbol == self.symbol

    def __hash__(self):
        return hash((self.company_name, self.symbol))

    def __ne__(self, other):
        return not (self == other)

    def __str__(self):
        return ",".join([self.company_name, self.symbol])

    def __repr__(self):
        return "".join(["[", ", ".join([self.company_name, self.symbol]), "]"])

    @staticmethod
    def company_name_search(meta, pattern, only_name=False):
        results = set()
        for company_obj in meta:
            if not company_obj:
                continue
            if (not only_name) and re.search(pattern, company_obj.symbol, re.IGNORECASE):
                results.add(company_obj)
            if re.search(
                pattern, company_obj.company_name, re.IGNORECASE
            ):
                results.add(company_obj)

        return results
