#!/usr/bin/env python

# THIS SCRIPT FOR DEBUGGING AND TESTING ONLY
# THIS SCRIPT FOR DEBUGGING AND TESTING ONLY
# THIS SCRIPT FOR DEBUGGING AND TESTING ONLY
# THIS SCRIPT FOR DEBUGGING AND TESTING ONLY

import nsysstats

class TESTReportSQLTable(nsysstats.Report):

    table_default = 'TARGET_INFO_GPU'

    usage = f"""{{SCRIPT}}[:<table_name>] -- Return Table

    <table_name> : The name of an SQLite table

    Output defined by <table_name>.

    This report accepts a database table (or view) name and
    executes the statement "SELECT * FROM <table_name>".  It is
    mostly for debugging/testing.  If no <table_name> is given,
    the table {table_default} will be used.
"""

    query_stub = "SELECT * FROM {TABLE}"

    def setup(self):
        err = super().setup()
        if err != None:
            return err

        table_name = self.table_default
        if len(self.args) > 0:
            table_name = self.args[0]

        if not self.table_exists(table_name):
            return f"{{DBFILE}} does not contain the table {table_name}"

        self.query = self.query_stub.format(TABLE=table_name)

if __name__ == "__main__":
    TESTReportSQLTable.Main()
