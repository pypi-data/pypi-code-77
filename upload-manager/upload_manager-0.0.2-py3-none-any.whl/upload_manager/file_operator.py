import csv
import io


class CSVFileWriter(object):

    def __init__(self, filename):
        self.csv_file = None
        self.writer = None
        self.open_file(filename)

    def open_file(self, filename):
        self.csv_file = io.StringIO()
        self.csv_file.name = filename
        self.writer = csv.writer(self.csv_file, lineterminator="\n")

    def close_writer(self):
        self.csv_file.close()

    def get_file_object(self):
        return self.csv_file

    def write_rows_to_file(self, data):
        """
        writes data into sheet
        :return:
        """
        self.writer.writerows(data)
