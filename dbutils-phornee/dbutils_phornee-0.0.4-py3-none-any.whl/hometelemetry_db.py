import sys
import mariadb
from datetime import datetime, timedelta

class DBOpenException(Exception):
    def __init__(self, message):
        # Call the base class constructor with the parameters it needs
        super().__init__(message)


class DBGetLockException(Exception):
    def __init__(self, message):
        # Call the base class constructor with the parameters it needs
        super().__init__(message)


class DBReleaseLockException(Exception):
    def __init__(self, message):
        # Call the base class constructor with the parameters it needs
        super().__init__(message)


class homeTelemetryDB:

    def __init__(self):
        self.conn = None

    def openConn(self, autocommit=True):
        """"""
        # Connect to MariaDB Platform
        try:
            self.conn = mariadb.connect(
                user="pi",
                password="i6B#Z*5Afvre",
                host="192.168.0.14",
                port=3306,
                database="hometelemetry"

            )
        except mariadb.Error as e:
            raise DBOpenException(f"Error connecting to MariaDB Platform: {e}")

        self.conn.autocommit = autocommit

        return self.conn

    def getConn(self):
        return self.conn

    def closeConn(self):
        self.conn.close()

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
            raise DBGetLockException(e)
