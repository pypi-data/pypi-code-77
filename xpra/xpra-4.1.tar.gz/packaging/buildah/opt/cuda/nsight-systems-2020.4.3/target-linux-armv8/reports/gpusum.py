#!/usr/bin/env python

import nsysstats

class CUDAGPUSummary(nsysstats.Report):

    ARG_BASE = 'base'

    usage = f"""{{SCRIPT}}[:{ARG_BASE}] -- GPU Summary (kernels + memory operations)

    {ARG_BASE} - Optional argument, if given, will cause summary to be over the
           base name of the kernel, rather than the templated name.

    Output: All time values given in nanoseconds
        Time(%) : Percentage of "Total Time"
        Total Time : The total time used by all executions of this kernel
        Instances: The number of executions of this object
        Average : The average execution time of this kernel
        Minimum : The smallest execution time of this kernel
        Maximum : The largest execution time of this kernel
        Category : The category of the operation
        Operation : The name of the kernel

    This report provides a summary of CUDA kernels and memory opreations,
    and their execution times. Note that the "Time(%)" column is calculated
    using a summation of the "Total Time" column, and represents that
    kernel's or memory operation's percent of the execution time of the
    kernels and memory operations listed, and not a percentage of the
    application wall or CPU execution time.

    This report combines data from the "gpukernsum" and "gpumemtimesum"
    reports.  This report is very similar to output of the command
    "nvprof --print-gpu-summary".
"""

    query_stub = """
WITH
    {MEM_OPER_STRS_CTE}
    gpuops AS (
        {GPU_SUB_QUERY}
    ),
    summary AS (
        SELECT
            name AS name,
            category AS category,
            sum(duration) AS total,
            count(*) AS num,
            avg(duration) AS avg,
            min(duration) AS min,
            max(duration) AS max
        FROM
            gpuops
        GROUP BY 1
    ),
    totals AS (
        SELECT sum(total) AS total
        FROM summary
    )
SELECT
    round(summary.total * 100.0 / totals.total, 1) AS "Time(%)",
    summary.total AS "Total Time (ns)",
    summary.num AS "Instances",
    round(summary.avg, 1) AS "Average",
    summary.min AS "Minimum",
    summary.max AS "Maximum",
    summary.category AS "Category",
    summary.name AS "Operation"
FROM
    summary
JOIN
    totals
ORDER BY 2 DESC
;
"""

    query_kernel = """
        SELECT
            str.value AS name,
            kern.end - kern.start AS duration,
            'CUDA_KERNEL' AS category
        FROM
            CUPTI_ACTIVITY_KIND_KERNEL AS kern
        LEFT OUTER JOIN
            StringIds AS str
            ON str.id = kern.{NAME_COL_NAME}
    """

    query_memcpy = """
        SELECT
            mos.name AS name,
            mcpy.end - mcpy.start AS duration,
            'MEMORY_OPER' AS category
        FROM
            CUPTI_ACTIVITY_KIND_MEMCPY as mcpy
        JOIN
            MemcpyOperStrs AS mos
            ON mos.id = mcpy.copyKind
    """

    query_memset = """
        SELECT
            '[CUDA memset]' AS name,
            end - start AS duration,
            'MEMORY_OPER' AS category
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

        name_col_name = 'demangledName'
        for arg in self.args:
            if arg == self.ARG_BASE:
                name_col_name = 'shortName'

        sub_queries = []

        if self.table_exists('CUPTI_ACTIVITY_KIND_KERNEL'):
            sub_queries.append(self.query_kernel.format(NAME_COL_NAME = name_col_name))

        if self.table_exists('CUPTI_ACTIVITY_KIND_MEMCPY'):
            sub_queries.append(self.query_memcpy)

        if self.table_exists('CUPTI_ACTIVITY_KIND_MEMSET'):
            sub_queries.append(self.query_memset)

        if len(sub_queries) == 0:
            return "{DBFILE} does not contain GPU kernel/memroy operations data."

        self.query = self.query_stub.format(
            MEM_OPER_STRS_CTE = self.MEM_OPER_STRS_CTE,
            GPU_SUB_QUERY = self.query_union.join(sub_queries))

if __name__ == "__main__":
    CUDAGPUSummary.Main()
