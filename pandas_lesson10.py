# conding: utf8
import pandas as pd
import os.path as op

"""
データの保存を色々なパターンで
さすがにsqlには吐き出せないみたいだけど、その他は基本ok
jsonもいけるのはかなり便利
"""

d = range(1, 10)
df = pd.DataFrame(d, columns=['Number'])

df.to_excel('Lesson10.xlsx', sheet_name='testing', index=False)

path = op.abspath('Lesson10.xlsx')
df = pd.read_excel(path, 0)

df.to_json('Lesson10.json')
jsonpath = op.abspath('Lesson10.json')
df2 = pd.read_json(jsonpath)
print df2