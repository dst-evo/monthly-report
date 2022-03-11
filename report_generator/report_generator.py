# import libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# import scripts
import calculations
import img_generator

# create dataframes from .csv-files for each machine
df_a = pd.read_csv(r'./aggregate_data/aggregate_data_a.csv', sep=';')
df_b = pd.read_csv(r'./aggregate_data/aggregate_data_b.csv', sep=';')
df_c = pd.read_csv(r'./aggregate_data/aggregate_data_c.csv', sep=';')
df_d = pd.read_csv(r'./aggregate_data/aggregate_data_d.csv', sep=';')

df_date = pd.to_datetime(df_a['date'])

# plot produced boxes per day and machine
img_generator.daily_barplot(df_b['produced_boxes'], df_a['produced_boxes'],
                            df_c['produced_boxes'], df_d['produced_boxes'], df_date)
