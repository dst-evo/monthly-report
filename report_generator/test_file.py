import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('./raw_data/Produced boxes_Total.csv', delimiter=';')

df = df[df['Machine'] == 'Total']

df['DateTime'] = pd.to_datetime(df['DateTime'])

plt.bar(df['DateTime'], df['Boxes'])

plt.xlabel('Date Time')
plt.xticks(rotation=45)

plt.show()

