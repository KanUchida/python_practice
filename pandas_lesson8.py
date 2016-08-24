import pandas as pd
import sys
from sqlalchemy import create_engine, MetaData, Table, select

"""
sqlと繋げる必要ないから
しばらく放っておく。
"""

conn = engine.connect()

metadata = MetaData(conn)

tbl = Table(TableName, metadata, autoload=True, schema='family')
tbl.create(checkfirst=True)

sql = tbl.select()

result = conn.execute(sql)

df = pd.DataFrame(data=list(result), column=result.keys())
conn.close()

