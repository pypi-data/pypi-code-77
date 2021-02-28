from sqlalchemy import Table, Boolean, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

Base = declarative_base()
session = None


class File(Base):
    __tablename__ = 'files'
    id = Column(Integer, primary_key=True)
    hash = Column(String, nullable=False)
    file = Column(String, nullable=False)
    packed = Column(Boolean, default=False, nullable=False)

    def add(hash: str, file: str) -> 'File':
        new_file = File(hash=hash, file=file)
        session.add(new_file)
        session.commit()
        return new_file


class Tag(Base):
    __tablename__ = 'tags'
    id = Column(Integer, primary_key=True)
    hash = Column(String, nullable=False)
    tag = Column(String, nullable=False)

    def add(hash: str, tag: str) -> 'Tag':
        new_tag = Tag(hash=hash, tag=tag)
        session.add(new_tag)
        session.commit()
        return new_tag


def bind(engine):
    global Base
    global session

    session = Session(engine)
    Base.metadata.create_all(engine)
