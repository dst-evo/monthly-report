# import libraries
import string
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager


# import scripts
import calculations
import img_generator

# create dataframes from .csv-files for each machine
df_a = pd.read_csv(r'./aggregate_data/aggregate_data_a.csv',
                   sep=';', parse_dates=['date'], index_col=['date'])
df_b = pd.read_csv(r'./aggregate_data/aggregate_data_b.csv', sep=';')
df_c = pd.read_csv(r'./aggregate_data/aggregate_data_c.csv', sep=';')
df_d = pd.read_csv(r'./aggregate_data/aggregate_data_d.csv', sep=';')

# plot produced boxes per day and machine
img_generator.single_linechart(df_b['produced_boxes'], df_a['produced_boxes'],
                               df_c['produced_boxes'], df_d['produced_boxes'], df_a.index)

img_generator.daily_barplot(df_b['produced_boxes'], df_a['produced_boxes'],
                            df_c['produced_boxes'], df_d['produced_boxes'], df_a.index)


# flist = matplotlib.font_manager.findSystemFonts(fontpaths=None, fontext='ttf')
# names = [matplotlib.font_manager.FontProperties(
#    fname=fname).get_name() for fname in flist]
#
# print(names)
