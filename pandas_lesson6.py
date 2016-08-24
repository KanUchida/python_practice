# coding: utf8
# http://nbviewer.jupyter.org/urls/bitbucket.org/hrojas/learn-pandas/raw/master/
#lessons/06%20-%20Lesson.ipynb

"""
groupby は難しい事考えないで、「何で注目したいか」ってのをそれでまとめればいい・
複数のgroupbyで指定した場合は。先に書いたものから後に書いたものへの入れ子構造になる
groupby しただけでは新しいobjectが作られるだけ、まとめたかったらsumで足し合わせる
"""

import pandas as pd
import sys

d = {'one': [1,1,1,1,1], 'two':[2,2,2,2,2], 'letter': ['a','a','b','b','c']}
df = pd.DataFrame(d)
print df

one = df.groupby('letter')
print one.sum()

letterone = df.groupby(['letter', 'one']).sum()
print letterone
print letterone.index

letterone = df.groupby(['letter', 'one'], as_index=False).sum()
print letterone

