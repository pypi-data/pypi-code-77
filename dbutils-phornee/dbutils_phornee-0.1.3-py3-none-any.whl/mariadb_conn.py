import mariadb
from datetime import datetime, timedelta
from .db_conn import DBConn, DBOpenException, DBGetLockException, DBReleaseLockException

class MariaDBConn(DBConn):

    def __init__(self):
        super().__init__()

    def openConn(self, params, autocommit=True):
        """"""
        # Connect to MariaDB Platform
        try:
            self.conn = mariadb.connect(**params)

        except mariadb.Error as e:
            raise DBOpenException(f"Error connecting to MariaDB Platform: {e}")

        self.conn.autocommit = autocommit

        return self.conn

    def closeConn(self):
        self.conn.close()

    def insert(self, table, params):
        try:
            cursor = self.conn.cursor()

            params_converted = {}
            for key, value in params.items():
                if isinstance(value, datetime):
                    params_converted[key] = value.strftime('%Y-%m-%d %H:%M:%S')
                else:
                    params_converted[key] = value

            sql = "INSERT INTO {tablename} ({columns}) VALUES {values};".format(
                tablename=table,
                columns=', '.join(params_converted.keys()),
                values=tuple(params_converted.values())
            )

            cursor.execute(sql)
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            raise Exception(e)

    def getLock(self, lockname):
        try:
            cursor = self.conn.cursor()

            sql = "SELECT * FROM lock WHERE name={} FOR UPDATE".format(lockname)
            cursor.execute(sql)
            res = cursor.fetchall()
            if cursor.rowcount == 1:
                if res[0][0] == 'idle':
                    sql = "UPDATE lock SET status='locked', timestamp = UTC_TIMESTAMP() WHERE name={}".format(lockname)
                    cursor.execute(sql)
                else:
                    if (datetime.utcnow() - res[0][1]) > timedelta(minutes=20):  #We assume that more than 20 minutes implies orphan lock
                        sql = "UPDATE lock SET timestamp = UTC_TIMESTAMP() WHERE name={}".format(lockname)
                        cursor.execute(sql)
                    else:
                        self.conn.rollback()
                        return False
            else:
                sql = "INSERT INTO lock VALUES ({}, 'unlocked', UTC_TIMESTAMP())".format(lockname)
                cursor.execute(sql)

        except Exception as e:
            self.conn.rollback()
            raise DBGetLockException(e)

        self.conn.commit()

        return True

    def releaseLock(self, lockname):
        try:
            cursor = self.conn.cursor()
            sql = "UPDATE lock SET status='unlocked', timestamp = UTC_TIMESTAMP() WHERE name={}".format(lockname)
            cursor.execute(sql)
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            raise DBReleaseLockException(e)
