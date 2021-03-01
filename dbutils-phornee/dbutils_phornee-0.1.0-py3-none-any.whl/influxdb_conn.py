from .db_conn import DBConn, DBOpenException, DBGetLockException, DBReleaseLockException


class InfluxDBConn(DBConn):

    def __init__(self):
        super().__init__()

    def openConn(self, params, autocommit=True):
        self.conn.autocommit = autocommit

    def closeConn(self):
        self.conn.close()

    def insert(self, table, params):
        pass

    def getLock(self, lockname):
        raise

    def releaseLock(self, lockname):
        raise

