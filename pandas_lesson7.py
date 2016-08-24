import pandas as pd

"""
統計の知識がたくさん出てきて難しい
grupbyの仕方によって平均も標準偏差も違ってくるから、そこは試行錯誤が必要
lambda のところは、Revenueカラムに対して働く（それしかcolumnがないから）
統計の正規分布とかその辺りの知識をもうちょっとつけたいと思った。
棄却域とかのあたりがいまいちわからぬ
"""

# Create a dataframe with dates as your index
States = ['NY', 'NY', 'NY', 'NY', 'FL', 'FL', 'GA', 'GA', 'FL', 'FL']
data = [1.0, 2, 3, 4, 5, 6, 7, 8, 9, 10]
idx = pd.date_range(start='1/1/2012', periods=10, freq='MS')
df1 = pd.DataFrame(data, index=idx, columns=['Revenue'])
df1['State'] = States

# Create a second dataframe
data2 = [10.0, 10.0, 9, 9, 8, 8, 7, 7, 6, 6]
idx2 = pd.date_range(start='1/1/2013', periods=10, freq='MS')
df2 = pd.DataFrame(data2, index=idx2, columns=['Revenue'])
df2['State']=States

df = pd.concat([df1, df2])

newdf = df.copy()
newdf['x-Mean'] = abs(newdf['Revenue'] - newdf['Revenue'].mean())
newdf['1.96*std'] = 1.96 * newdf['Revenue'].std()
newdf['Outlier'] = abs(newdf['Revenue'] - newdf['Revenue'].mean()) > 1.96 * newdf['Revenue'].std()

# method2
newdf = df.copy()
State = newdf.groupby('State')

newdf['Outlier'] = State.transform(lambda x: abs(x - x.mean()) > 1.96 * x.std())
newdf['x-Mean'] = State.transform(lambda x: abs(x - x.mean()))
newdf['1.96*std'] = State.transform(lambda x: 1.96 * x.std())

# method3
newdf = df.copy()

StateMonth = newdf.groupby(['State', lambda x: x.month])
newdf['Outlier'] = StateMonth.transform(lambda x: abs(x-x.mean()) > 1.96*x.std())
newdf['x-Mean'] = StateMonth.transform(lambda x: abs(x-x.mean()))
newdf['1.96*std'] = StateMonth.transform(lambda x: 1.96*x.std())

# method4
newdf = df.copy()

def s(group):
    group['x-Mean'] = abs(group['Revenue'] - group['Revenue'].mean())
    group['1.96*std'] = 1.96 * group['Revenue'].std()
    group['Outlier'] = abs(group['Revenue'] - group['Revenue'].mean()) > 1.96 * group['Revenue'].std()
    return group

Newdf2 = State.apply(s)

# method 5

newdf = df.copy()
State = newdf.groupby('State')

newdf['Lower'] = State['Revenue'].transform(lambda x: x.quantile(q=.25) - (1.5*(x.quantile(q=.75) - x.quantile(q=.25))))
newdf['Upper'] = State['Revenue'].transform(lambda x: x.quantile(q=.25) + (1.5*(x.quantile(q=.75)-x.quantile(q=.25))))
newdf['Outlier'] = (newdf['Revenue'] < newdf['Lower']) | (newdf['Revenue'] > newdf['Upper'])
print newdf