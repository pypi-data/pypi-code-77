#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pytest

from bapy import cmd
from bapy import IPLoc
from bapy import IPv4
from bapy import mongocol
from bapy import MongoColMotor
from bapy import MongoColPy
from bapy import MongoConn
from bapy import mongodb
from bapy import MongoDBMotor
from bapy import MongoDBPy
from bapy import MongoIP
from bapy import Obj
from bapy.data.test_addr import google_addr
from bapy.data.test_addr import google_name

db_name = 'pytest'
col_name = 'test'
data = {db_name: col_name}

cmd('mongossh.sh')


def test_col():
    for connection in MongoConn:
        assert isinstance(mongodb(db_name, True, conn=connection), MongoDBPy)

        if col_name in mongodb(db_name, True, conn=connection).list_collection_names():
            mongocol(col_name, True, conn=connection).drop()

        mongocol(col_name, True, conn=connection).insert_one(data)
        assert isinstance(mongocol(col_name, True, conn=connection), MongoColPy)
        assert db_name in mongocol(col_name, True, conn=connection).find_one(data)
        mongocol(col_name, True, conn=connection).drop()


@pytest.mark.asyncio
async def test_col_aio():
    for connection in MongoConn:
        assert isinstance(mongodb(db_name, conn=connection), MongoDBMotor)

        if col_name in await mongodb(db_name, conn=connection).list_collection_names():
            await mongocol(col_name, conn=connection).drop()

        await mongocol(col_name, conn=connection).insert_one(data)
        assert isinstance(mongocol(col_name, conn=connection), MongoColMotor)
        assert db_name in await mongocol(col_name, conn=connection).find_one(data)
        await mongocol(col_name, conn=connection).drop()


def test_mongoip():
    one = MongoIP(_id=google_addr, _db='test', _connection=MongoConn.LOCAL)
    isinstance(one._id, IPv4)
    isinstance(one.loc, IPLoc)
    assert one.name == google_name
    assert one.col.name == MongoIP.__class__.__name__
    one.col.drop()
    assert one.find_self == dict()
    rv = one.update_self

@pytest.mark.asyncio
async def test_mongoip_aio():
    one = MongoIP(_id=google_addr, _db='test')
    isinstance(one._id, IPv4)
    isinstance(one.loc, IPLoc)
    assert one.name == google_name
    assert await one.col_aio.name == MongoIP.__class__.__name__
    await one.col.drop()
    assert await one.find_self_aio == dict()
    rv = await one.update_self_aio


