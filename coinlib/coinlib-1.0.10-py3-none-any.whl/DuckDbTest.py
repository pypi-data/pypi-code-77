import importlib
from IPython import get_ipython
from coinlib.helper import in_ipynb
from coinlib.helper import pip_install_or_ignore
import subprocess
import sys
import timeit
import math
import time

#CHART_DATA_INFLUXDB_HOST="116.203.110.177"
#CHART_DATA_INFLUXDB_DB="coindeck-chartdata"
#CHART_DATA_INFLUXDB_USER="coindeck"
#CHART_DATA_INFLUXDB_PWD="6j8l0gbxsNkpAQXuL8C9"

CHART_DATA_INFLUXDB_HOST="localhost"
CHART_DATA_INFLUXDB_DB="coindeck-chartdata"
CHART_DATA_INFLUXDB_USER=""
CHART_DATA_INFLUXDB_PWD=""

pip_install_or_ignore("influxdb", "influxdb")
pip_install_or_ignore("redis", "redis")
pip_install_or_ignore("tables", "tables")
pip_install_or_ignore("duckdb", "duckdb")

import redis
import sqlalchemy
import pandas as pd

import pyarrow as pa

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from TimescaleDatabase import TimescaleDatabase
from influxdb import DataFrameClient
from influxdb import InfluxDBClient
from timeit import default_timer as timer
from datetime import timedelta
import sqlite3
import pyarrow.parquet as pq
"""
#influxClient.query(query)
dfclient = DataFrameClient(CHART_DATA_INFLUXDB_HOST, 8086,
                                   CHART_DATA_INFLUXDB_USER, CHART_DATA_INFLUXDB_PWD, CHART_DATA_INFLUXDB_DB)

start = time.time()
data_result = dfclient.query('select * from "' + CHART_DATA_INFLUXDB_DB + '"."autogen"."' + "5fa5dfdd34b8ec2c25523852" + '"')
df = data_result["5fa5dfdd34b8ec2c25523852"]

end = time.time()
print(end - start)

print(df)
"""

import duckdb
import io

con = duckdb.connect(database=':duckdb:test.duck', read_only=False)

start = time.time()
rel = con.execute("SELECT * FROM parquet_scan('testpeople1.parquet');")
new_df = rel.df()
print(new_df)

end = time.time()
print("read all column data", end - start)

for n in range(100):
    start = time.time()
    f = io.BytesIO()

    table = pa.Table.from_pandas(new_df)
    pq.write_table(table, f)

    #new_df.to_parquet(f)

    f.seek(0,0)
    import requests
    res = requests.post(url='http://localhost:8091/collection/asd'+str(n)+'/insertRaw',
                        files={"data": f.getvalue()},
                        headers={"Content-Type": 'application/octet-stream'})
    f.close()
    end = time.time()
    print("7mb to binary data", end - start)

"""
start = time.time()
#con.execute("ALTER TABLE people2 ALTER __index_level_0__ TYPE TIMESTAMP;")

con.execute("ALTER TABLE people2 DROP \"ema_1:y\"")

end = time.time()
print("drop and write data", end - start)
"""


start = time.time()
#con.execute("ALTER TABLE people2 ALTER __index_level_0__ TYPE TIMESTAMP;")
df = con.execute("SELECT * FROM people2").fetchdf()
print(df)

end = time.time()
print("read data", end - start)

