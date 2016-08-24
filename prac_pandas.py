import pandas as pd
import numpy as np

dates = pd.date_range('20130102', periods=6)
df = pd.DataFrame(np.random.randn(6,4), index=dates, columns=list('ABCD'))

df2 = pd.DataFrame({'A':1,
'B':pd.Timestamp('20130102'),
'C':pd.Series(1, index=list(range(4)), dtype='float32'),
'D':np.array([3]*4, dtype='int32'),
'E':pd.Categorical(['test', 'train', 'test', 'train']),
'F':'foo'})

print df2.dtypes

# Viewing Data
"""
print df.head()
print df.tail(3)
print df.index
print df.index, 'index'
print df.columns, 'columns'
print df.values, 'values'
print df.describe()
print df.T, 'df.T'
"""