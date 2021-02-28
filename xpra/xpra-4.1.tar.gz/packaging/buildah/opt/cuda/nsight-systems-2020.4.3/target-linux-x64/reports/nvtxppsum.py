#!/usr/bin/env python

import nsysstats

class NVTXPushPopSummary(nsysstats.Report):

    EVENT_TYPE_NVTX_DOMAIN_CREATE = 75
    EVENT_TYPE_NVTX_PUSHPOP_RANGE = 59
    EVENT_TYPE_NVTXT_PUSHPOP_RANGE = 70

    usage = f"""{{SCRIPT}} -- NVTX Push/Pop Range Summary

    No arguments.

    Output: All time values given in nanoseconds
        Time(%) : Percentage of "Total Time"
        Total Time : The total time used by all instances of this range
        Instances: The number of instances of this range
        Average : The average execution time of this range
        Minimum : The smallest execution time of this range
        Maximum : The largest execution time of this range
        Range : The name of the range

    This report provides a summary of NV Tools Extensions Push/Pop Ranges and
    their execution times. Note that the "Time(%)" column is calculated
    using a summation of the "Total Time" column, and represents that
    range's percent of the execution time of the ranges listed,
    and not a percentage of the application wall or CPU execution time.
"""

    query = f"""
WITH
    domains AS (
        SELECT
            domainId AS id,
            text AS name
        FROM
            NVTX_EVENTS
        WHERE
            eventType = {EVENT_TYPE_NVTX_DOMAIN_CREATE}
    ),
    maxts AS(
        SELECT max(max(start), max(end)) AS m
        FROM   NVTX_EVENTS
    ),
    nvtx AS (
        SELECT
            coalesce(ne.end, (SELECT m FROM maxts)) - ne.start AS duration,
            CASE
                WHEN d.name NOT NULL AND sid.value IS NOT NULL
                    THEN d.name || ':' || sid.value
                WHEN d.name NOT NULL AND sid.value IS NULL
                    THEN d.name || ':' || ne.text
                WHEN d.name IS NULL AND sid.value NOT NULL
                    THEN sid.value
                ELSE ne.text
            END AS tag
        FROM
            NVTX_EVENTS AS ne
        LEFT OUTER JOIN
            domains AS d
            ON (ne.domainId = d.id)
        LEFT OUTER JOIN
            StringIds AS sid
            ON (ne.textId = sid.id)
        WHERE
            ne.eventType = {EVENT_TYPE_NVTX_PUSHPOP_RANGE}
            OR
            ne.eventType = {EVENT_TYPE_NVTXT_PUSHPOP_RANGE}
    ),
    summary AS (
        SELECT
            tag AS name,
            sum(duration) AS total,
            count(*) AS num,
            avg(duration) AS avg,
            min(duration) AS min,
            max(duration) AS max
        FROM
            nvtx
        GROUP BY 1
    ),
    totals AS (
        SELECT sum(total) AS total
        FROM summary
    )

    SELECT
        round(total * 100.0 / (SELECT total FROM totals), 1) AS "Time(%)",
        total AS "Total Time (ns)",
        num AS "Instances",
        round(avg, 1) AS "Average",
        min AS "Minimum",
        max AS "Maximum",
        name AS "Range"
    FROM
        summary
    ORDER BY 2 DESC
;
"""

    table_checks = {
        'NVTX_EVENTS':
            "{DBFILE} does not contain NV Tools Extension (NVTX) data"
    }

if __name__ == "__main__":
    NVTXPushPopSummary.Main()
