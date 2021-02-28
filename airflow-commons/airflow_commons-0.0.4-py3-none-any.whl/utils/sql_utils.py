from google.cloud import bigquery

from airflow_commons.utils.bigquery_utils import query_information_schema
from airflow_commons.utils.file_utils import read_sql
from airflow_commons.glossary import *
from airflow_commons.sql_resources import (
    DEDUPLICATION_SOURCE_STATEMENT_SQL_FILE,
    UPSERT_SQL_FILE,
    INSERT_SQL_FILE,
    DEDUPLICATION_SQL_FILE,
    DELETE_SQL_FILE,
)

DML_MODES = ["INSERT", "UPSERT", "DEDUPLICATE"]


def get_column_list_and_update_statements(
    client: bigquery.Client, project_id: str, dataset_id: str, table_id: str
):
    """
    Gets column list from information schema and prepares column list and update statements for further queries

    :param client: Client needed for API request
    :param project_id: Bigquery project id
    :param dataset_id: dataset id
    :param table_id: table id
    :return: columns, update_statements strings
    """
    statements = dict()
    columns_list = query_information_schema(
        client=client,
        requested_column_name="column_name",
        project_id=project_id,
        dataset_id=dataset_id,
        table_name=table_id,
    )
    statements["columns"] = COMMA.join(columns_list)
    statements["update_statements"] = COMMA.join(
        [i + EQUALS_SIGN + SOURCE_PREFIX + i for i in columns_list]
    )
    return statements


def get_primary_key_statements(primary_keys):
    """
    Gets group by clause and merge keys based on given primary key list, for further usage on queries

    :param primary_keys: list of primary key columns
    :return: sql group by and merge keys
    """
    statements = dict()
    statements["primary_key_list"] = COMMA.join(primary_keys)
    statements["merge_keys"] = (AND + WHITE_SPACE).join(
        [
            TARGET_PREFIX + i + EQUALS_SIGN + SOURCE_PREFIX + i + WHITE_SPACE
            for i in primary_keys
        ]
    )
    return statements


def get_order_by_statement(time_columns):
    """
    Gets order by statement based on given datetime columns, for further usage on queries

    :param time_columns: list of datetime columns
    :return: sql order by values, ordering rows descending by given columns
    """
    return COMMA.join([i + WHITE_SPACE + DESCENDING for i in time_columns])


def get_deduplication_source_statement(
    start_date: str,
    end_date: str,
    project_id: str,
    source_dataset: str,
    source_table: str,
    source_partition_field: str,
    target_partition_field: str,
    oldest_target_partition: str,
    primary_keys: list,
    time_columns: list,
):
    """
    Prepares deduplication source statement that will be used on deduplication process

    :param start_date: deduplication time interval start
    :param end_date: deduplication time interval end
    :param project_id: Bigquery project id
    :param source_dataset: source dataset id
    :param source_table: source table id
    :param source_partition_field: source table's partition column name
    :param target_partition_field: target table's partition column name
    :param oldest_target_partition: oldest value of target table's partition column
    :param primary_keys: primary key column list
    :param time_columns: time columns list to order rows
    :return: formatted source statement
    """
    group_by_clause = get_primary_key_statements(primary_keys)["primary_key_list"]
    order_by_clause = get_order_by_statement(time_columns)
    return read_sql(
        sql_file=DEDUPLICATION_SOURCE_STATEMENT_SQL_FILE,
        order_by_clause=order_by_clause,
        project_id=project_id,
        source_dataset=source_dataset,
        source_table=source_table,
        source_partition_field=source_partition_field,
        start_date=start_date,
        end_date=end_date,
        target_partition_field=target_partition_field,
        oldest_target_partition=oldest_target_partition,
        group_by_clause=group_by_clause,
    )


def get_merge_sql(
    client,
    project_id,
    target_dataset,
    target_table,
    source_statement,
    primary_keys,
    mode: str,
    **kwargs
):
    """
    Returns a merge sql with given parameters.

    :param client: Bigquery client
    :param project_id: Bigquery project id
    :param target_dataset: target dataset id
    :param target_table: target table id
    :param source_statement: source statement part of merge query
    :param primary_keys: primary keys of the target table
    :param mode: query mode, can take values "DEDUPLICATE", "INSERT", and "UPSERT"
    :param kwargs:
    :return: merge query
    """
    if mode not in DML_MODES:
        raise ValueError(
            "Invalide dml mode: {}. Acceptaple modes are ".format(mode)
            + COMMA.join(i for i in DML_MODES)
        )
    sql_params = get_column_list_and_update_statements(
        client, project_id, target_dataset, target_table
    )
    sql_params["merge_keys"] = get_primary_key_statements(primary_keys)["merge_keys"]
    sql_file = UPSERT_SQL_FILE
    if mode == "INSERT":
        sql_params.pop("update_statements")
        sql_file = INSERT_SQL_FILE
    elif mode == "DEDUPLICATE":
        sql_file = DEDUPLICATION_SQL_FILE
    return read_sql(
        sql_file=sql_file,
        project_id=project_id,
        target_dataset=target_dataset,
        target_table=target_table,
        source_statement=source_statement,
        **sql_params,
        **kwargs
    )


def get_oldest_partition_field_sql(
    sql_file: str,
    project_id: str,
    target_dataset: str,
    target_table: str,
    source_dataset: str,
    source_table: str,
    target_partition_field: str,
    source_partition_field: str,
    start_date: str,
    end_date: str,
    primary_keys: list,
):
    """
    Queries source table and returns the oldest value target table's partition column

    :param sql_file: relative location of sql file
    :param project_id: Bigquery project id
    :param target_dataset: target dataset id
    :param target_table: target table id
    :param source_dataset: source dataset id
    :param source_table: source table id
    :param target_partition_field: time partitioning column of target table
    :param source_partition_field: time partitioning column of source table
    :param start_date: query start date
    :param end_date: query end date
    :param primary_keys: primary key columns of the source and target tables
    :return:
    """
    return read_sql(
        sql_file=sql_file,
        project_id=project_id,
        target_dataset=target_dataset,
        target_table=target_table,
        source_dataset=source_dataset,
        source_table=source_table,
        target_partition_field=target_partition_field,
        source_partition_field=source_partition_field,
        start_date=start_date,
        end_date=end_date,
        primary_key_list=get_primary_key_statements(primary_keys)["primary_key_list"],
    )


def get_delete_sql(
    project_id,
    dataset_id,
    table_id,
    where_statement,
):
    return read_sql(
        sql_file=DELETE_SQL_FILE,
        project_id=project_id,
        dataset_id=dataset_id,
        table_id=table_id,
        where_statement=where_statement,
    )
