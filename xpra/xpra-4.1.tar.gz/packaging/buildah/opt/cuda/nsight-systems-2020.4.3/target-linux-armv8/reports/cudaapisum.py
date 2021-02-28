#!/usr/bin/env python

import nsysstats

class CUDAAPISummary(nsysstats.Report):

    usage = f"""{{SCRIPT}} -- CUDA API Summary

    No arguments.

    Output: All time values given in nanoseconds
        Time(%) : Percentage of "Total Time"
        Total Time : The total time used by all executions of this function
        Num Calls: The number of calls to this function
        Average : The average execution time of this function
        Minimum : The smallest execution time of this function
        Maximum : The largest execution time of this function
        Name : The name of the function

    This report provides a summary of CUDA API functions and their
    execution times. Note that the "Time(%)" column is calculated
    using a summation of the "Total Time" column, and represents that
    function's percent of the execution time of the functions listed,
    and not a percentage of the application wall or CPU execution time.
"""

    query = """
WITH
    summary AS (
        SELECT
            nameId AS nameId,
            sum(end - start) AS total,
            count(*) AS num,
            avg(end - start) AS avg,
            min(end - start) AS min,
            max(end - start) AS max
        FROM
            CUPTI_ACTIVITY_KIND_RUNTIME
        GROUP BY 1
    ),
    totals AS (
        SELECT sum(total) AS total
        FROM summary
    )
SELECT
    round(summary.total * 100.0 / totals.total, 1) AS "Time(%)",
    summary.total AS "Total Time (ns)",
    summary.num AS "Num Calls",
    round(summary.avg, 1) AS "Average",
    summary.min AS "Minimum",
    summary.max AS "Maximum",
    CASE substr(ids.value, -6, 2)
        WHEN '_v'
            THEN substr(ids.value, 1, length(value)-6)
        ELSE ids.value
    END AS "Name"
FROM
    summary
CROSS JOIN
    totals
INNER JOIN
    StringIds AS ids
    ON ids.id = summary.nameId
ORDER BY 2 DESC
;
"""

    table_checks = {
        'CUPTI_ACTIVITY_KIND_RUNTIME':
            '{DBFILE} does not contain CUDA trace data'
    }

if __name__ == "__main__":
    CUDAAPISummary.Main()
