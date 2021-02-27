from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


def init_db(dbhost, dbuser, dbpass, dbname):
    """Parameters:
    db_host: Hostname of PostgreSQL DB,
    db_user: Username of PostgreSQL DB,
    dbpass: Password of PostgreSQL DB,
    dbname: Database Name of PostgreSQL DB

    Returns: engine, Base, get_db
    Please Note: JWT tokens are made from email attribute in User.
    """
    SQLALCHEMY_DATABASE_URL = "postgresql://" + \
        dbuser + ":"+dbpass+"@"+dbhost+"/"+dbname
    engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_pre_ping=True)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base = declarative_base()

    def get_db():
        try:
            db = SessionLocal()
            yield db
        finally:
            db.close()
    return engine, Base, get_db
