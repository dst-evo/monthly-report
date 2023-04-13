# This is Version 2 of the famous Report Generator
# The general Idea of the programm is the same as before
# generating a comprehenisve Report about the current 
# Status of the Packing Machines used by Digitec Galaxus AG.
# Most of the used data is from "Current Month - 1" but some
# Values are compared month over month and year over year.
#
# Required Libraries can be found in "requirements.txt"
# Since there is currently no API available for the Dashboard
# the Data has to be downloaded manually.
#
# writen by dominic stalder (mailto:dominic.stalder@proton.me)
# with help of some special people

# load Libraries
#------------------------------------------------------------------------------
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.colors as colors
from matplotlib.lines import Line2D
#------------------------------------------------------------------------------

# set global plt parameters 
#------------------------------------------------------------------------------
plt.rcParams['figure.figsize'] = [16.0, 9.0]
plt.rcParams['figure.dpi'] = 300
plt.rcParams['font.family'] = 'Europa-Regular'
plt.rcParams['axes.grid'] = True
plt.rcParams['axes.grid.axis'] = 'y'
plt.rcParams['axes.axisbelow'] = True
plt.rcParams['legend.frameon'] = False
plt.rcParams['legend.loc'] = 'upper center'
plt.rcParams['lines.linewidth'] = 3.5
plt.rcParams['font.size'] = 22
#------------------------------------------------------------------------------

# define colors and names for the plots
#------------------------------------------------------------------------------
# define color map
palette_lc = colors.ListedColormap(
    ['#FDE725', '#7AD151', '#22A884', '#2A788E', '#414487', 'grey'])

palette_list = (['#FDE725', '#7AD151', '#22A884',
                '#2A788E', '#414487', 'grey'])

# define legend style
custom_lines = [Line2D([0], [0], color=palette_lc(0), lw=8),
                Line2D([0], [0], color=palette_lc(1), lw=8),
                Line2D([0], [0], color=palette_lc(2), lw=8),
                Line2D([0], [0], color=palette_lc(3), lw=8)]
machine_names = ['L1 - VPM B (4958)', 'L2 - VPM A (4959)',
                 'L3 - VPM C (4960)', 'L4 - VPM D (4961)']
#------------------------------------------------------------------------------

# read csv files from local storage
#------------------------------------------------------------------------------
df_current = pd.read_csv('./raw_data/boxes_total_current.csv', delimiter=';', usecols=['DateTime', 'Machine', 'Boxes']) 
df_previous = pd.read_csv('./raw_data/boxes_total_previous.csv', delimiter=';', usecols=['DateTime', 'Machine', 'Boxes'])
#------------------------------------------------------------------------------


# Plot total Boxes Year over Year
#------------------------------------------------------------------------------
# Filter rows where Machine is 'Total'
df_current = df_current[df_current['Machine'] == 'Total']
df_previous = df_previous[df_previous['Machine'] == 'Total']

# Convert DateTime column to pandas datetime format
df_current['DateTime'] = pd.to_datetime(df_current['DateTime'])
df_previous['DateTime'] = pd.to_datetime(df_previous['DateTime'])

# Add a year to the DateTime column in df_previous
df_previous['DateTime'] = df_previous['DateTime'] + pd.offsets.DateOffset(years=1)

# Merge the two dataframes based on DateTime column
df_merged = pd.merge(df_current, df_previous, on='DateTime')

# Rename the columns to differentiate between the two sets of boxes
df_merged = df_merged.rename(columns={'Boxes_x': 'Boxes_current', 'Boxes_y': 'Boxes_previous'})

# Extract the values for the desired time period
start_date = pd.to_datetime('2022-04-01')
end_date = pd.to_datetime('2023-03-01')
df_period = df_merged[(df_merged['DateTime'] >= start_date) & (df_merged['DateTime'] < end_date)]

# Group by month and year and sum Boxes values for each month and year
df_period_monthly = df_period.groupby(pd.Grouper(key='DateTime', freq='M')).sum()

# Create a grouped bar chart comparing the boxes in each month
labels = df_period_monthly.index.strftime('%b')
x = np.arange(len(labels))
width = 0.35  # the width of the bars

fig, ax = plt.subplots()
rects1 = ax.bar(x - width/2, df_period_monthly['Boxes_current'], width, label='Current')
rects2 = ax.bar(x + width/2, df_period_monthly['Boxes_previous'], width, label='Previous')

# Add y-axis label and legend
ax.set_ylabel('Boxes')
ax.legend()

# Add text labels to each column
for rect in rects1 + rects2:
    height = rect.get_height()
    ax.text(rect.get_x() + rect.get_width() / 2, height, int(height),
            ha='center', va='bottom')

# Set tick labels and title
ax.set_xticks(x)
ax.set_xticklabels(labels, rotation=45, ha='right')
ax.set_title('Comparison of Boxes by Month and Year')

# Show the plot
plt.show()

# TODO: save plot as pdf to use it in the report

#------------------------------------------------------------------------------


