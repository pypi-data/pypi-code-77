# auto generated by update_py.py
from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from ..config import Configurator
from ..utils import singleton


@singleton
class DatabaseConnector(object):

    def __init__(self, db=None, debug_mode=False):
        self._debug_mode = debug_mode

        self._db_config = Configurator().get_db_settings()
        if db is not None:
            self._db_config.db = db
        self._db_conn_str = self._db_config.to_conn_str()
        self.log('connecting to', self._db_config)

        self._engine = None
        self._session_maker = None
        self._scoped_session_maker = None

        self._connect()

    def log(self, *args):
        if self._debug_mode:
            msg = ' '.join([str(a) for a in args])
            print(msg)

    def _connect(self):
        self._engine = create_engine(self._db_conn_str, pool_pre_ping=True)
        self._session_maker = sessionmaker(bind=self._engine)
        self._scoped_session_maker = scoped_session(self._session_maker)

    @contextmanager
    def get_session(self, scoped=True, managed=True):
        if self._engine is None:
            self._connect()
        session = self._scoped_session_maker() if scoped else self._session_maker()
        yield session
        if managed:
            session.close()

    def get_engine(self):
        if self._engine is None:
            self._connect()
        return self._engine

    def __str__(self):
        return str(self._db_config)


def test_connection():
    from .models import Account
    with DatabaseConnector(db='db_core').get_session() as session:
        accounts = session.query(Account).all()
        print(accounts)


if __name__ == '__main__':
    test_connection()
