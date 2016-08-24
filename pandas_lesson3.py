# coding: utf8
# http://nbviewer.jupyter.org/urls/bitbucket.org/hrojas/learn-pandas/raw/master/lessons/03%20-%20Lesson.ipynb

import glob
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib

# set seed
np.random.seed(111)

def CreateDataSet(Number=1):
    Output = []
    for i in range(Number):
        # create a weekyl date range
        rng = pd.date_range(start='1/1/2009', end='12/31/2012', freq='W-MON')

        # Create random data 
        data = np.random.randint(low=25, high=1000, size=len(rng))

        # status pool
        status = [1, 2, 3]

        # Make a random list of statuses
        random_status = [status[np.random.randint(low=0, high=len(status))] for i in range(len(rng))]

        # state pool
        states = ['GA', 'FL', 'fl', 'NY', 'NJ', 'TX']

        # Make a random list of states
        ranodm_states = [states[np.random.randint(low=0, high=len(states))] for i in range(len(rng))]

        Output.extend(zip(ranodm_states, random_status, data, rng))
    return Output

dataset = CreateDataSet(4)
df = pd.DataFrame(data=dataset, columns=['States', 'Status', 'CustomerCount', 'StatusDate'])

df.to_excel('Lesson3.xlsx', index=False)
path = glob.glob('./Lesson3.xlsx')
df = pd.read_excel(path[0], 0, index_col='StatusDate')

df['States'] = df.States.apply(lambda x:x.upper())

mask = df['Status'] == 1
df = df[mask]


# この指定の仕方を覚えておくとすごく楽
# where でややこしく書いてた部分がこれで治せる
mask = df.States == 'NJ'
df['States'][mask] = 'NY'

sortdf = df[df['States'] == 'NY'].sort_index(axis=0)

Daily = df.reset_index().groupby(['States', 'StatusDate']).sum()
del Daily['Status']
"""
Daily.loc['FL']['2012':].plot()
plt.title('FL')
Daily.loc['GA']['2012':].plot()
plt.title('GA')
Daily.loc['NY']['2012':].plot()
plt.title('NY')
Daily.loc['TX']['2012':].plot()
plt.title('TX')
plt.show()
"""

# このデータの扱い方もすごい
# 条件をLower と Upperで用意
# そこに収まらないやつを Falseにする
# それを最後の行に足してあげる
# そこがFalseのものだけとれば、該当範囲内のものが撮れる
# 株価のやつもこのやり方をするとすごく楽だった
StateYearMonth = Daily.groupby([Daily.index.get_level_values(0), Daily.index.get_level_values(1).year, Daily.index.get_level_values(1).month])
Daily['Lower'] = StateYearMonth['CustomerCount'].transform(lambda x: x.quantile(q=.25) - (1.5*x.quantile(q=.75) - x.quantile(q=.25)))
Daily['Upper'] = StateYearMonth['CustomerCount'].transform(lambda x: x.quantile(q=.75) + (1.5*x.quantile(q=.75) - x.quantile(q=.25)))
Daily['Outlier'] = (Daily['CustomerCount'] < Daily['Lower']) | (Daily['CustomerCount'] > Daily['Upper'])
Daily = Daily[Daily['Outlier'] == False]

ALL = pd.DataFrame(Daily['CustomerCount'].groupby(Daily.index.get_level_values(1)).sum())
ALL.columns = ['CustomerCount'] # rename column

YearMonth = ALL.groupby([lambda x:x.year, lambda x: x.month])
ALL['Max'] = YearMonth['CustomerCount'].transform(lambda x: x.max())

data = [1000, 2000, 3000]
idx = pd.date_range(start='12/31/2011', end='12/31/2013', freq='A')
BHAG = pd.DataFrame(data, index=idx, columns=['BHAG'])

combined = pd.concat([ALL, BHAG], axis=0)
combined = combined.sort_index(axis=0)

# fig, axes =plt.subplots(figsize=(12, 7))

combined['BHAG'].fillna(method='pad').plot(color='green', label='BHAG')
# combined['Max'].plot(color='blue', label='All Markets')

Year = combined.groupby(lambda x: x.year).max()
Year['YR_PCT_Change'] = Year['Max'].pct_change(periods=1)
# print (1 + Year.ix[2012,'YR_PCT_Change']) * Year.ix[2012,'Max']

# Graph

ALL['Max'].plot(figsize=(10, 5))
plt.title('ALL Markets')

fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(20, 10))
fig.subplots_adjust(hspace=1.0)

Daily.loc['FL']['CustomerCount']['2012':].fillna(method='pad').plot(ax=axes[0,0])
Daily.loc['GA']['CustomerCount']['2012':].fillna(method='pad').plot(ax=axes[0,1])
Daily.loc['TX']['CustomerCount']['2012':].fillna(method='pad').plot(ax=axes[1,0])
Daily.loc['NY']['CustomerCount']['2012':].fillna(method='pad').plot(ax=axes[1,1])

# Add titles
axes[0, 0].set_title('Florida')
axes[0, 1].set_title('Georgia')
axes[1, 0].set_title('Texas')
axes[1, 1].set_title('North East')

plt.show()