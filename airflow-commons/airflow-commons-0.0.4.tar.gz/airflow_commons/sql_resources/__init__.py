import os


here = os.path.abspath(os.path.dirname(__file__))


ARCHIVE_DELETE_WHERE_STATEMENT_FILE = os.path.join(
    here, "bigquery/archive/archive_delete_where_statement.sql"
)
ARCHIVE_SOURCE_STATEMENT_FILE = os.path.join(
    here, "bigquery/archive/archive_source_statement.sql"
)
DEDUPLICATION_SOURCE_STATEMENT_SQL_FILE = os.path.join(
    here, "bigquery/deduplication/deduplication_source_statement.sql"
)
DEDUPLICATION_SQL_FILE = os.path.join(here, "bigquery/deduplication/deduplicate.sql")
DELETE_SQL_FILE = os.path.join(here, "bigquery/dml/delete.sql")
GET_COLUMN_NAMES_SQL_FILE = os.path.join(
    here, "bigquery/information_schema/get_column_names.sql"
)
GET_OBJECT_FIELDS_SQL_FILE = os.path.join(
    here, "bigquery/information_schema/get_object_fields.sql"
)
GET_OLDEST_PARTITION_FIELD_SQL_FILE = os.path.join(
    here, "bigquery/deduplication/get_oldest_partition_field.sql"
)
GET_TABLE_NAMES_SQL_FILE = os.path.join(
    here, "bigquery/information_schema/get_table_names.sql"
)
INSERT_SQL_FILE = os.path.join(here, "bigquery/dml/insert.sql")
UPSERT_SQL_FILE = os.path.join(here, "bigquery/dml/upsert.sql")
