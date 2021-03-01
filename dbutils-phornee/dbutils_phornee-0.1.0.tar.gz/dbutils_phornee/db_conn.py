from abc import ABC, abstractmethod

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


class DBConn(ABC):

    def __init__(self):
        self.conn = None

    @abstractmethod
    def openConn(self, params, autocommit=True):
        pass

    @abstractmethod
    def getConn(self):
        return self.conn

    def closeConn(self):
        pass

    @abstractmethod
    def insert(self, table, params):
        pass

    def getLock(self, lockname):
        raise

    def releaseLock(self, lockname):
        raise

