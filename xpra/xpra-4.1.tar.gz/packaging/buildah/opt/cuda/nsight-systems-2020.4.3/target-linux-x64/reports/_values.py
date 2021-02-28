#!/usr/bin/env python

# THIS SCRIPT FOR DEBUGGING AND TESTING ONLY
# THIS SCRIPT FOR DEBUGGING AND TESTING ONLY
# THIS SCRIPT FOR DEBUGGING AND TESTING ONLY
# THIS SCRIPT FOR DEBUGGING AND TESTING ONLY

import nsysstats

class TESTReportSQLValues(nsysstats.Report):

    value_default = [1]

    usage = f"""{{SCRIPT}}[:<v>[:<v>]...] -- Return Provided Values

    <v> : One or more values

    Output:
        Value : the values passed in as <v>

    This report accepts one or more values, <v> and returns those
    values as a single column data set.  It is mostly for
    debugging/testing.  If no <v> is given, the single value
    "{value_default[0]}" will be used.  The SQLite file is not
    used or accessed, other than for verification.
"""

    query_stub = """
    WITH VAL_CTE (VALUE) AS ( VALUES {VALUES} )
    SELECT VALUE AS VALUE FROM VAL_CTE
"""

    def setup(self):
        err = super().setup()
        if err != None:
            return err

        values = self.value_default
        if len(self.args) > 0:
            values = self.args

        self.query = self.query_stub.format(VALUES = ",".join(["('{v}')".format(v=val) for val in values]))

if __name__ == "__main__":
    TESTReportSQLValues.Main()
