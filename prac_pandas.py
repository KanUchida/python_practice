# coding: utf8
import pandas as pd
import matplotlib.pyplot as plt
import numpy.random as np

def CreateDataSet(Number=1):

    Output = []

    for i in range(Number):
        rng = pd.date_range(start='1/1/2009', end='12/31/2012', freq='W-MON')

        data = np.randint(low=25, high=1000, size=len(rng))

        status=[1, 2, 3]
        random_status = [status[np.randint(low=0, high=len(status))] for i in range(len(rng))]

        states = ['GA', 'FL', 'fl', 'NY', 'NJ', 'TX']

        random_states = [states[np.randint(low=0, high=len(states))] for i in range(len(rng))]

        Output.extend(zip(random_states, random_status, data, rng))

    return Output

dataset = CreateDataSet(4)
df = pd.DataFrame(data=dataset, columns=['State', 'Status', 'CustomerCount', 'StatusDate'])

df.to_excel('Lesson3.xlsx', index=False)
df = pd.read_excel('./Lesson3.xlsx', 0, index_col='StatusDate')

df['State'] = df.State.apply(lambda x: x.upper())

mask = df['Status'] == 1
df = df[mask]

mask = df.State == 'NJ'
df['State'][mask] = 'NY'

sortdf = df[df['State'] == 'NY'].sort_index(axis=0)

Daily = df.reset_index().groupby(['State', 'StatusDate']).sum()
del Daily['Status']

fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(20,10))

StateYearMonth = Daily.groupby([Daily.index.get_level_values(0), Daily.index.get_level_values(1).year, Daily.index.get_level_values(1).month])
Daily['Lower'] = StateYearMonth['CustomerCount'].transform(lambda x: x.quantile(q=.25) - (1.5*x.quantile(q=.75) - x.quantile(q=.25)))
Daily['Upper'] = StateYearMonth['CustomerCount'].transform(lambda x: x.quantile(q=.75) + (1.5*x.quantile(q=.75)-x.quantile(q=.25)))
Daily['Outlier'] = (Daily['CustomerCount'] < Daily['Lower']) | (Daily['CustomerCount'] > Daily['Upper'])
Daily = Daily[Daily['Outlier'] == False]

# 州に関係なく送る
ALL = pd.DataFrame(Daily['CustomerCount'].groupby(Daily.index.get_level_values(1)).sum())
YearMonth = ALL.groupby([lambda x:x.year, lambda x: x.month])

ALL['Max'] = YearMonth['CustomerCount'].transform(lambda x: x.max())
print ALL.head

data = [1000, 2000, 3000]
idx = pd.date_range(start='12/31/2011', end='12/31/2013', freq='A')
BHAG = pd.DataFrame(data, index=idx, columns =['BHAG'])

combined = pd.concat([ALL, BHAG], axis=0)
combined = combined.sort_index(axis=0)

fig, axes = plt.subplots(figsize=(12, 7))

combined['BHAG'].fillna(method='pad').plot(color='green', label='BHAG')
combined['Max'].plot(color='blue', label='ALL markets')
plt.legend(loc='best')
plt.show()