#!/usr/bin/env python

# THIS SCRIPT FOR DEBUGGING AND TESTING ONLY
# THIS SCRIPT FOR DEBUGGING AND TESTING ONLY
# THIS SCRIPT FOR DEBUGGING AND TESTING ONLY
# THIS SCRIPT FOR DEBUGGING AND TESTING ONLY

import nsysstats

class TESTReportSQLStatement(nsysstats.Report):

    usage = f"""{{SCRIPT}}[:<sql_statement>] -- Run SQL Statement

    <sql_statement> : an arbitrary SQLite statement

    Output defined by <sql_statement>.

    This report accepts and executes an arbitrary SQL statement.
    It is mostly for debugging/testing.  If no <sql_statement> is
    given, the statement "{nsysstats.Report.query}" is executed.
"""

    def setup(self):
        err = super().setup()
        if err != None:
            return err

        if len(self.args) > 0:
            self.query = self.args[0]

if __name__ == "__main__":
    TESTReportSQLStatement.Main()
