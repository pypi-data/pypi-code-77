#!/usr/bin/env python

import nsysstats

class CUDAGPUKernelSummary(nsysstats.Report):

    ARG_BASE = 'base'

    usage = f"""{{SCRIPT}}[:{ARG_BASE}] -- CUDA GPU Kernel Summary

    {ARG_BASE} - Optional argument, if given, will cause summary to be over the
           base name of the kernel, rather than the templated name.

    Output: All time values given in nanoseconds
        Time(%) : Percentage of "Total Time"
        Total Time : The total time used by all executions of this kernel
        Instances: The number of calls to this kernel
        Average : The average execution time of this kernel
        Minimum : The smallest execution time of this kernel
        Maximum : The largest execution time of this kernel
        Name : The name of the kernel

    This report provides a summary of CUDA kernels and their
    execution times. Note that the "Time(%)" column is calculated
    using a summation of the "Total Time" column, and represents that
    kernel's percent of the execution time of the kernels listed,
    and not a percentage of the application wall or CPU execution time.
"""

    query_stub = """
WITH
    summary AS (
        SELECT
            {NAME_COL_NAME} AS nameId,
            sum(end - start) AS total,
            count(*) AS num,
            avg(end - start) AS avg,
            min(end - start) AS min,
            max(end - start) AS max
        FROM
            CUPTI_ACTIVITY_KIND_KERNEL
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
    ids.value AS "Name"
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
        'CUPTI_ACTIVITY_KIND_KERNEL':
            '{DBFILE} does not contain CUDA kernel data'
    }

    def setup(self):
        err = super().setup()
        if err != None:
            return err

        name_col_name = 'demangledName'
        for arg in self.args:
            if arg == self.ARG_BASE:
                name_col_name = 'shortName'

        self.query = self.query_stub.format(NAME_COL_NAME = name_col_name)

if __name__ == "__main__":
    CUDAGPUKernelSummary.Main()
