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
# -----------------------------------------------------------------------------
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.colors as colors
import seaborn as sns
from matplotlib.lines import Line2D
# -----------------------------------------------------------------------------

# set global plt parameters
# -----------------------------------------------------------------------------
plt.rcParams['figure.figsize'] = [16.0, 9.0]  # [16.0, 9.0]
plt.rcParams['figure.dpi'] = 300
plt.rcParams['font.family'] = 'Europa-Regular'
plt.rcParams['axes.grid'] = True
plt.rcParams['axes.grid.axis'] = 'y'
plt.rcParams['axes.axisbelow'] = True
plt.rcParams['legend.frameon'] = False
plt.rcParams['legend.loc'] = 'upper center'
plt.rcParams['lines.linewidth'] = 3.5
plt.rcParams['font.size'] = 22
# -----------------------------------------------------------------------------

# define colors and names for the plots
# -----------------------------------------------------------------------------
# define color map
palette_lc = colors.ListedColormap(
    ['#FDE725',
     '#7AD151',
     '#22A884',
     '#2A788E',
     '#414487',
     'grey',
     ])

palette_list = ['#FDE725',
                '#7AD151',
                '#22A884',
                '#2A788E',
                '#414487',
                'grey',
                ]

# define legend style
custom_lines = [Line2D([0], [0], color=palette_lc(0), lw=8),
                Line2D([0], [0], color=palette_lc(1), lw=8),
                Line2D([0], [0], color=palette_lc(2), lw=8),
                Line2D([0], [0], color=palette_lc(3), lw=8),
                ]
machine_names = ['L1 - VPM B (4958)',
                 'L2 - VPM A (4959)',
                 'L3 - VPM C (4960)',
                 'L4 - VPM D (4961)',
                 ]
# -----------------------------------------------------------------------------

# read csv files from local storage
# -----------------------------------------------------------------------------
df_current = pd.read_csv('./raw_data/boxes_total_current.csv',
                         delimiter=';',
                         usecols=['DateTime',
                                  'Machine',
                                  'Boxes',
                                  ],
                         )
df_previous = pd.read_csv('./raw_data/boxes_total_previous.csv',
                          delimiter=';',
                          usecols=['DateTime',
                                   'Machine',
                                   'Boxes',
                                   ],
                          )
# -----------------------------------------------------------------------------


# Plot total Boxes Year over Year
# -----------------------------------------------------------------------------
# Filter rows where Machine is 'Total'
df_current = df_current[df_current['Machine'] == 'Total']
df_previous = df_previous[df_previous['Machine'] == 'Total']

# Convert DateTime column to pandas datetime format
df_current['DateTime'] = pd.to_datetime(df_current['DateTime'])
df_previous['DateTime'] = pd.to_datetime(df_previous['DateTime'])

# Add a year to the DateTime column in df_previous
df_previous['DateTime'] = df_previous['DateTime'] + \
    pd.offsets.DateOffset(years=1)

# Merge the two dataframes based on DateTime column
df_merged = pd.merge(df_current, df_previous, on='DateTime')

# Rename the columns to differentiate between the two sets of boxes
df_merged = df_merged.rename(
    columns={'Boxes_x': 'Boxes_current', 'Boxes_y': 'Boxes_previous'})

# Extract the values for the desired time period
start_date = pd.to_datetime('2022-04-01')
end_date = pd.to_datetime('2023-03-01')
df_period = df_merged[(df_merged['DateTime'] >= start_date)
                      & (df_merged['DateTime'] < end_date)]

# Group by month and year and sum Boxes values for each month and year
df_period_monthly = df_period.groupby(
    pd.Grouper(key='DateTime', freq='M')).sum()

# Create a grouped bar chart comparing the boxes in each month
labels = df_period_monthly.index.strftime('%b')
x = np.arange(len(labels))
width = 0.35  # the width of the bars

fig, ax = plt.subplots()
# create the two bars
rects1 = ax.bar(
    x - width/2,
    df_period_monthly['Boxes_previous'],
    width,
    color=palette_list[5],
    label='Previous',
)
rects2 = ax.bar(
    x + width/2,
    df_period_monthly['Boxes_current'],
    width,
    color=palette_list[4],
    label='Current',
)
# Add y-axis label and legend
ax.set_ylabel('Boxes')
box = ax.get_position()
ax.set_position([box.x0,
                 box.y0 + box.height * 0.2,
                 box.width,
                 box.height * 0.8],
                )
ax.legend(['Previous', 'Current'],
          bbox_to_anchor=(0.5, -0.15),
          ncol=2,
          )

# Add text labels to each column
for rect in rects1 + rects2:
    height = rect.get_height()
    ax.text(rect.get_x() + rect.get_width() / 2,
            height,
            int(height),
            ha='center',
            va='bottom',
            fontsize=16,
            )

# Set tick labels and title
ax.set_xticks(x)
ax.set_xticklabels(labels,
                   rotation=45,
                   ha='right',
                   )
ax.set_title('Comparison of Boxes by Month')

plt.box(False)
# Show the plot
plt.savefig('./test_1.pdf')
# plt.show()
plt.clf()

# TODO: save plot as pdf to use it in the report
# -----------------------------------------------------------------------------

# Make a donut Chart with all Machines and plot the total in the middle
# -----------------------------------------------------------------------------
# Filter the rows to include only the desired machines
df_donut = pd.read_csv('./raw_data/boxes_total_current.csv',
                       delimiter=';',
                       usecols=['DateTime',
                                'Machine',
                                'Boxes',
                                ],
                       )

# Filter the rows to include only the last available month
df_donut['DateTime'] = pd.to_datetime(df_donut['DateTime'])
last_month = df_donut['DateTime'].max()
df_last_month = df_donut[df_donut['DateTime'] == last_month]

# Filter the rows to include only the desired machines
df_machines = df_last_month[df_last_month['Machine'].isin(machine_names)]

# Calculate the total number of boxes for the selected machines
total_boxes = df_machines['Boxes'].sum()

# Create a pie chart with the selected machines
colors = [c for c in palette_list if c != 'grey']
fig, ax = plt.subplots()
wedges, texts, autotexts = ax.pie(df_machines['Boxes'],
                                  labels=df_machines['Machine'],
                                  colors=colors,
                                  autopct='%1.1f%%',
                                  startangle=90,
                                  textprops={'fontsize': 14},
                                  wedgeprops={'linewidth': 7,
                                              'edgecolor': 'white',
                                              }
                                  )
center_circle = plt.Circle((0, 0),
                           0.5,
                           color='white',
                           )
fig = plt.gcf()
fig.gca().add_artist(center_circle)
plt.setp(autotexts,
         size=16,
         weight="bold",
         )
plt.setp(texts,
         size=16,
         )

# Add the total number of boxes to the center of the chart
ax.text(0,
        0,
        total_boxes,
        ha='center',
        va='center',
        fontsize=24,
        )

# Set the title of the chart
ax.set_title('Total Boxes for Selected Machines ({})'.format(
    last_month.strftime('%b %Y')),
    fontsize=20,
)

# set axis equal to ensure circle is drawn as a circle
plt.axis('equal')
# Show the chart
plt.savefig('./test_2.pdf')
# plt.show()
plt.clf()
# -----------------------------------------------------------------------------


# create a single line chart that shows the total daily produced boxes
# -----------------------------------------------------------------------------
df = pd.read_csv('./raw_data/produced_boxes_daily.csv',
                 delimiter=';',
                 usecols=['DateTime',
                          'Machine',
                          'Boxes',
                          ],
                 )

# format DateTime to dd/mm
df['DateTime'] = pd.to_datetime(df['DateTime'])
df['DateTime'] = df['DateTime'].dt.strftime('%d/%m')

# filter for Total Values
total_df = df[df['Machine'] == 'Total']

# create the line plot, move the legend to the bottom
fig, ax = plt.subplots()
total_df.plot(x='DateTime', y='Boxes', color=palette_list[4], ax=ax)
box = ax.get_position()
ax.set_position([box.x0, box.y0 + box.height * 0.2,
                 box.width, box.height * 0.8,
                 ],
                )
ax.legend(['Total'],
          bbox_to_anchor=(0.5, -0.15),
          ncol=1,
          )
plt.box(False)
plt.xticks(rotation=45)

# shot the chart
plt.savefig('./test_3.pdf')
# plt.show()
plt.clf()
# -----------------------------------------------------------------------------


# create a grouped barplot showing daily produced boxes per machine
# -----------------------------------------------------------------------------
# Load data from CSV file
df = pd.read_csv('./raw_data/produced_boxes_daily.csv',
                 delimiter=';',
                 usecols=['DateTime',
                          'Machine',
                          'Boxes'],
                 )

# Format DateTime to dd/mm
df['DateTime'] = pd.to_datetime(df['DateTime'])
df['DateTime'] = df['DateTime'].dt.strftime('%d/%m')

# Create grouped barplot with legend at bottom
fig, ax = plt.subplots()
sns.barplot(x='DateTime',
            y='Boxes',
            hue='Machine',
            palette=palette_list,
            data=df[df['Machine'].isin(machine_names)],
            ax=ax,
            )
box = ax.get_position()
ax.set_position([box.x0, box.y0 + box.height * 0.2,
                 box.width, box.height * 0.8,
                 ])
ax.legend(bbox_to_anchor=(0.5, -0.15),
          ncol=4,
          )

plt.box(False)
plt.xticks(rotation=45)

# show the chart
plt.savefig('./test_4.pdf')
# plt.show()
plt.clf()
