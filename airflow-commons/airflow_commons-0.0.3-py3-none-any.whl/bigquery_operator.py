from airflow_commons.utils.bigquery_utils import *
from airflow_commons.logger import LOGGER
from airflow_commons.utils.sql_utils import (
    get_deduplication_source_statement,
    get_merge_sql,
)
from airflow_commons.utils.file_utils import read_sql
from airflow_commons.utils.time_utils import get_buffered_timestamp

WRITE_DISPOSITIONS = ["WRITE_APPEND", "WRITE_TRUNCATE", "WRITE_EMPTY"]

DEFAULT_PRIMARY_KEYS = ["id"]
DEFAULT_TIME_COLUMNS = ["last_updated_at", "processed_at"]


def deduplicate(
    service_account_file: str,
    start_date: str,
    end_date: str,
    project_id: str,
    source_dataset: str,
    source_table: str,
    target_dataset: str,
    target_table: str,
    primary_keys=None,
    time_columns=None,
    timeout=DEFAULT_TIMEOUT,
    location=DEFAULT_LOCATION,
):
    """
    Runs a merge query to deduplicate rows in historic table, and write to target snapshot table

    :param service_account_file: relative location of service account json
    :param start_date: deduplication interval start
    :param end_date: deduplication interval end
    :param project_id: Bigquery project id
    :param source_dataset: source dataset id
    :param source_table: source table id
    :param target_dataset: target dataset id
    :param target_table: target table id
    :param primary_keys: primary key columns of the source and target tables
    :param time_columns: time columns list to order rows
    :param timeout: query timeout duration parameter
    :param location: query location parameter
    :return:
    """
    client = connect(service_account_file)
    if primary_keys is None:
        primary_keys = DEFAULT_PRIMARY_KEYS
    if time_columns is None:
        time_columns = DEFAULT_TIME_COLUMNS
    buffered_start_date = get_buffered_timestamp(start_date)
    source_partition_field = get_time_partition_field(
        client, source_dataset, source_table
    )
    target_partition_field = get_time_partition_field(
        client, target_dataset, target_table
    )
    oldest_target_partition = get_oldest_partition_field(
        client,
        source_dataset,
        source_table,
        target_partition_field,
        source_partition_field,
        buffered_start_date,
        end_date,
    )
    if oldest_target_partition:
        source_statement = get_deduplication_source_statement(
            start_date=buffered_start_date,
            end_date=end_date,
            project_id=project_id,
            source_dataset=source_dataset,
            source_table=source_table,
            source_partition_field=source_partition_field,
            target_partition_field=target_partition_field,
            oldest_target_partition=oldest_target_partition,
            primary_keys=primary_keys,
            time_columns=time_columns,
        )
        sql = get_merge_sql(
            client=client,
            project_id=project_id,
            target_dataset=target_dataset,
            target_table=target_table,
            source_statement=source_statement,
            primary_keys=primary_keys,
            mode="DEDUPLICATE",
            target_partition_field=target_partition_field,
            oldest_target_partition=oldest_target_partition,
        )
        query(
            client=client,
            job_config=bigquery.QueryJobConfig(),
            sql=sql,
            timeout=timeout,
            location=location,
        )
    else:
        LOGGER(
            "There is no data: - {project_id}.{source_dataset}.{source_table} - between [{start_date} - {end_date}] .".format(
                project_id=project_id,
                source_dataset=source_dataset,
                source_table=source_table,
                start_date=buffered_start_date,
                end_date=end_date,
            )
        )


def upsert(
    service_account_file: str,
    source_statement_file: str,
    project_id: str,
    target_dataset: str,
    target_table: str,
    source_statement_params: dict = None,
    primary_keys=None,
    timeout=DEFAULT_TIMEOUT,
    location=DEFAULT_LOCATION,
):
    """
    Runs a merge query to upsert target table, with given source statement, merge conditions, and primary keys

    :param service_account_file: relative location of service account json
    :param source_statement_file: relative location of source statement file
    :param project_id: Bigquery project id
    :param target_dataset: targeted dataset id
    :param target_table: targeted table id
    :param source_statement_params: parameters of source statement
    :param primary_keys: target table's primary key list
    :param timeout: query timeout duration in seconds
    :param location: query location parameter
    :return:
    """
    client = connect(service_account_file)
    if source_statement_params is None:
        source_statement_params = dict()
    if primary_keys is None:
        primary_keys = DEFAULT_PRIMARY_KEYS
    source_statement = read_sql(
        sql_file=source_statement_file, **source_statement_params
    )
    sql = get_merge_sql(
        client=client,
        project_id=project_id,
        target_dataset=target_dataset,
        target_table=target_table,
        source_statement=source_statement,
        primary_keys=primary_keys,
        mode="UPSERT",
    )
    query(
        client=client,
        job_config=bigquery.QueryJobConfig(),
        sql=sql,
        timeout=timeout,
        location=location,
    )


def insert(
    service_account_file: str,
    source_statement_file: str,
    project_id: str,
    target_dataset: str,
    target_table: str,
    source_statement_params: dict = None,
    primary_keys=None,
    timeout=DEFAULT_TIMEOUT,
    location=DEFAULT_LOCATION,
):
    """
    Runs a merge query to insert non-existing rows to target table, with given source statement, merge conditions, and primary keys

    :param service_account_file: relative location of service account json
    :param source_statement_file: relative location of source statement file
    :param project_id: Bigquery project id
    :param target_dataset: targeted dataset id
    :param target_table: targeted table id
    :param source_statement_params: parameters of source statement
    :param primary_keys: target table's primary key list
    :param timeout: query timeout duration in seconds
    :param location: query location parameter
    :return:
    """
    client = connect(service_account_file)
    if source_statement_params is None:
        source_statement_params = dict()
    if primary_keys is None:
        primary_keys = DEFAULT_PRIMARY_KEYS
    source_statement = read_sql(
        sql_file=source_statement_file, **source_statement_params
    )
    sql = get_merge_sql(
        client=client,
        project_id=project_id,
        target_dataset=target_dataset,
        target_table=target_table,
        source_statement=source_statement,
        primary_keys=primary_keys,
        mode="INSERT",
    )
    query(
        client=client,
        job_config=bigquery.QueryJobConfig(),
        sql=sql,
        timeout=timeout,
        location=location,
    )


def write_query_results_to_destination(
    credentials_file: str,
    sql_file: str,
    timeout: int,
    location: str,
    destination_dataset: str,
    destination_table: str,
    write_disposition: str,
):
    """

    :param credentials_file: relative location of service account file
    :param sql_file: relative location of sql file to read sql from
    :param timeout: job timeout parameter
    :param location: job location parameter
    :param destination_dataset: id of the destination dataset
    :param destination_table: id of the destination table
    :param write_disposition: write disposition of query results
    :return:
    """
    if write_disposition not in WRITE_DISPOSITIONS:
        raise ValueError(
            "Invalid write disposition: {}. Acceptable values are WRITE_APPEND, WRITE_TRUNCATE, and WRITE_EMPTY".format(
                write_disposition
            )
        )
    client = connect(credentials_file)
    job_config = bigquery.QueryJobConfig()
    job_config.write_disposition = write_disposition
    job_config.allow_large_results = True
    job_config.destination = get_table_ref(
        client, destination_dataset, destination_table
    )
    sql = read_sql(sql_file=sql_file)
    query(client, job_config, sql, timeout, location)


def get_query_results(
    credentials_file: str,
    sql_file: str,
    sql_params: dict = None,
    timeout=DEFAULT_TIMEOUT,
    location=DEFAULT_TIMEOUT,
):
    """
    Runs query and returns the result as dataframe

    :param credentials_file: relative location of service account file
    :param sql_file: relative location of sql file to read sql from
    :param sql_params: sql parameters dictionary
    :param timeout: query timeout duration in seconds
    :param location: query location parameter
    :return: query result
    """
    client = connect(credentials_file=credentials_file)
    if sql_params is None:
        sql_params = dict()
    sql = read_sql(sql_file=sql_file, **sql_params)
    return query(
        client=client,
        job_config=bigquery.QueryJobConfig(),
        sql=sql,
        timeout=timeout,
        location=location,
    ).to_dataframe()


def get_single_value_query_results(
    credentials_file: str,
    sql_file: str,
    sql_params: dict = None,
    timeout=DEFAULT_TIMEOUT,
    location=DEFAULT_TIMEOUT,
):
    """
    Runs a single value returning query and returns the result

    :param credentials_file: relative location of service account file
    :param sql_file: relative location of sql file to read sql from
    :param sql_params: sql parameters dictionary
    :param timeout: query timeout duration in seconds
    :param location: query location parameter
    :return: query result
    """
    client = connect(credentials_file=credentials_file)
    if sql_params is None:
        sql_params = dict()
    sql = read_sql(sql_file=sql_file, **sql_params)
    return single_value_select(
        client=client,
        sql=sql,
        timeout=timeout,
        location=location,
    )
