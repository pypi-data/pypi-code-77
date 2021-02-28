#!/usr/bin/env python

import nsysstats

class CUDAGPUMemoryTimeSummary(nsysstats.Report):

    usage = f"""{{SCRIPT}} -- GPU Memory Operations Summary (by Time)

    No arguments.

    Output: All time values given in nanoseconds
        Time(%) : Percentage of "Total Time"
        Total Time : The total time used by all executions of this operation
        Operations: The number of operations to this type
        Average : The average execution time of this operation
        Minimum : The smallest execution time of this operation
        Maximum : The largest execution time of this operation
        operation : The name of the memory operation

    This report provides a summary of GPU memory operations and
    their execution times. Note that the "Time(%)" column is calculated
    using a summation of the "Total Time" column, and represents that
    operation's percent of the execution time of the operations listed,
    and not a percentage of the application wall or CPU execution time.
"""

    query_stub = """
WITH
    {MEM_OPER_STRS_CTE}
    memops AS (
        {MEM_SUB_QUERY}
    ),
    summary AS (
        SELECT
            name AS name,
            sum(duration) AS total,
            count(*) AS num,
            avg(duration) AS avg,
            min(duration) AS min,
            max(duration) AS max
        FROM
            memops
        GROUP BY 1
    ),
    totals AS (
        SELECT sum(total) AS total
        FROM summary
    )
SELECT
    round(summary.total * 100.0 / totals.total, 1) AS "Time(%)",
    summary.total AS "Total Time (ns)",
    summary.num AS "Operations",
    round(summary.avg, 1) AS "Average",
    summary.min AS "Minimum",
    summary.max AS "Maximum",
    summary.name AS "Operation"
FROM
    summary
JOIN
    totals
ORDER BY 2 DESC
;
"""

    query_memcpy = """
        SELECT
            mos.name AS name,
            mcpy.end - mcpy.start AS duration
        FROM
            CUPTI_ACTIVITY_KIND_MEMCPY as mcpy
        INNER JOIN
            MemcpyOperStrs AS mos
            ON mos.id = mcpy.copyKind
"""

    query_memset = """
        SELECT
            '[CUDA memset]' AS name,
            end - start AS duration
        FROM
            CUPTI_ACTIVITY_KIND_MEMSET
"""

    query_union = """
        UNION ALL
"""

    def setup(self):
        err = super().setup()
        if err != None:
            return err

        sub_queries = []

        if self.table_exists('CUPTI_ACTIVITY_KIND_MEMCPY'):
            sub_queries.append(self.query_memcpy)

        if self.table_exists('CUPTI_ACTIVITY_KIND_MEMSET'):
            sub_queries.append(self.query_memset)

        if len(sub_queries) == 0:
            return "{DBFILE} does not contain GPU memroy data."

        self.query = self.query_stub.format(
            MEM_OPER_STRS_CTE = self.MEM_OPER_STRS_CTE,
            MEM_SUB_QUERY = self.query_union.join(sub_queries))

if __name__ == "__main__":
    CUDAGPUMemoryTimeSummary.Main()
