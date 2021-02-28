#!/usr/bin/env python

import nsysstats

class CUDAGPUMemorySizeSummary(nsysstats.Report):

    usage = f"""{{SCRIPT}} -- GPU Memory Operations Summary (by Size)

    No arguments.

    Output: All memory values given in KiB
        Total : Total number of KiB utilized by this operation
        Operations : Number of executions of this operation
        Average : The average memory size of this operation
        Minimum : The smallest memory size of this operation
        Maximum : The largest memory size of this operation
        Name : The name of the operation

    This report provides a summary of GPU memory operations and
    the amount of memory they utilize.
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
            sum(size) AS total,
            count(*) AS num,
            avg(size) AS avg,
            min(size) AS min,
            max(size) AS max
        FROM memops
        GROUP BY 1
    )
SELECT
    printf('%.3f', summary.total/1024.0, 3) AS "Total",
    summary.num AS "Operations",
    printf('%.3f', summary.avg/1024.0, 3) AS "Average",
    printf('%.3f', summary.min/1024.0, 3) AS "Minimum",
    printf('%.3f', summary.max/1024.0, 3) AS "Maximum",
    summary.name AS "Operation"
FROM
    summary
ORDER BY 1 DESC
;
"""

    query_memcpy = """
        SELECT
            mos.name AS name,
            mcpy.bytes AS size
        FROM
            CUPTI_ACTIVITY_KIND_MEMCPY as mcpy
        INNER JOIN
            MemcpyOperStrs AS mos
            ON mos.id = mcpy.copyKind
"""

    query_memset = """
        SELECT
            '[CUDA memset]' AS name,
            bytes AS size
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
            return "{DBFILE} does not contain GPU memory data."

        self.query = self.query_stub.format(
            MEM_OPER_STRS_CTE = self.MEM_OPER_STRS_CTE,
            MEM_SUB_QUERY = self.query_union.join(sub_queries))

if __name__ == "__main__":
    CUDAGPUMemorySizeSummary.Main()
