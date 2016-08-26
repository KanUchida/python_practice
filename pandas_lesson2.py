import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


names = ['Bob', 'Jessica', 'Mary', 'John', 'Mel']
random_names = [names[np.random.randint(low=0, high=len(names))] for i in range(1000)]

births = [np.random.randint(low=0, high=1000) for i in range(1000)]

BabyDataSet = list(zip(random_names, births))

df = pd.DataFrame(data=BabyDataSet, columns=['Names', 'Births'])
df.to_csv('biths1880.csv', index=False, header=False)
df = pd.read_csv('./biths1880.csv', names=['Names', 'Births'])

name = df.groupby('Names')
df = name.sum()
Sorted = df.sort_values(['Births'], ascending=False)

df['Births'].plot.bar()
plt.show()