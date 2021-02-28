#!/usr/bin/env python

# THIS SCRIPT FOR DEBUGGING AND TESTING ONLY
# THIS SCRIPT FOR DEBUGGING AND TESTING ONLY
# THIS SCRIPT FOR DEBUGGING AND TESTING ONLY
# THIS SCRIPT FOR DEBUGGING AND TESTING ONLY

import nsysstats

class TESTReportSQLFile(nsysstats.Report):

    usage = f"""{{SCRIPT}}:<sql_file> -- Run SQL statement from file

    <sql_file> : File with SQL statement(s)

    Output defined by <sql_file>.

    This report executes an arbitrary SQL statement found in the given
    filename.  It is mostly for debugging/testing.  If no <sql_file> is
    given, or if the file does not exist or cannot be opened, an error
    is returned.  The file should contain only a single SQL statement.
"""

    query = "SELECT 1 AS 'ONE'"

    def setup(self):
        err = super().setup()
        if err != None:
            return err

        if len(self.args) != 1:
            return 'No filename given';
        try:
            with open(self.args[0], "r") as file:
                self.query = file.read()
        except EnvironmentError:
            return f"File {self.args[0]} could not be opened"

if __name__ == "__main__":
    TESTReportSQLFile.Main()
