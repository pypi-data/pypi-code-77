#!/usr/bin/env python

import nsysstats

class OpenMPEventSummary(nsysstats.Report):

    usage = f"""{{SCRIPT}} -- OpenMP Event Summary

    No arguments.

    Output: All time values given in nanoseconds
        Time(%) : Percentage of "Total Time"
        Total Time : The total time used by all executions of event type
        Count: The number of event type
        Average : The average execution time of event type
        Minimum : The smallest execution time of event type
        Maximum : The largest execution time of event type
        Name : The name of the event

    This report provides a summary of OpenMP events and their
    execution times. Note that the "Time(%)" column is calculated
    using a summation of the "Total Time" column, and represents that
    event type's percent of the execution time of the events listed,
    and not a percentage of the application wall or CPU execution time.
"""

    query_stub = """
WITH
    summary AS (
        {OPEN_MP_UNION}
    ),
    totals AS (
        SELECT sum(total) AS total
        FROM summary
    )
SELECT
    round(summary.total * 100.0 / totals.total, 1) AS "Time(%)",
    summary.total AS "Total Time (ns)",
    summary.num AS "Count",
    round(summary.avg, 1) AS "Average",
    summary.min AS "Minimum",
    summary.max AS "Maximum",
    ids.value AS "Name"
FROM
    summary
JOIN
    totals
LEFT JOIN
    StringIds AS ids
    ON ids.id = summary.nameId
ORDER BY 2 DESC
;
"""

    query_omp = """
        SELECT
            nameId AS nameId,
            count(*) AS num,
            min(end - start) AS min,
            max(end - start) AS max,
            avg(end - start) AS avg,
            sum(end - start) AS total
        FROM {TABLE}
        GROUP BY 1
"""

    query_union = """
        UNION ALL
"""

    def setup(self):
        err = super().setup()
        if err != None:
            return err

        omp_tables = self.search_tables(r'^OPENMP_EVENT_KIND_.+$')
        if len(omp_tables) == 0:
            return "{DBFILE} does not contain OpenMP event data."

        omp_queries = list(self.query_omp.format(TABLE=t) for t in omp_tables)
        self.query = self.query_stub.format(OPEN_MP_UNION = self.query_union.join(omp_queries))

if __name__ == "__main__":
    OpenMPEventSummary.Main()
