import cx_Oracle

class OracleConnection:
    def __init__(self, user, password, database):
        self.connection = cx_Oracle.connect(
            user,
            password,
            database
        )

    def __enter__(self):
        return self.connection

    def __exit__(self, exception_type, exception_value, traceback):
        self.connection.close()


def truncate_statement(
    table): return f'truncate table {table.schema}.{table.name}'


def generate_placeholders(i): return ','.join(
    [f':{n + 1}' for n in range(i)])


def insert_statement(
    table): return f'insert into {table.schema}.{table.name}({",".join(table.cols)}) values({generate_placeholders(len(table.cols))})'


def truncate_data(connection, table):
    with connection.cursor() as cursor:
        cursor.execute(truncate_statement(table))
        connection.commit()


def insert_data(connection, table, rows):
    with connection.cursor() as cursor:
        cursor.executemany(
            insert_statement(table),
            rows,
            batcherrors=True
        )

        connection.commit()

        errors = []
        for error in cursor.getbatcherrors():
            errors.append(error)

        return errors, cursor.rowcount


def call_procedure(connection, name, args=()):
    with connection.cursor() as cursor:
        cursor.callproc(name, args)
        connection.commit()

def execute_sql(connection, sql, args=()):
    with connection.cursor() as cursor:
        cursor.execute(sql, args)
        connection.commit()