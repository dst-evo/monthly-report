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
import new_image_generator as ig
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

# configure start and enddates
# -----------------------------------------------------------------------------
start_date = pd.to_datetime('2022-04-01')
end_date = pd.to_datetime('2023-03-01')
# -----------------------------------------------------------------------------

# import all csv files
# -----------------------------------------------------------------------------
# df_current = pd.read_csv('./raw_data/boxes_total_current.csv',
#                         delimiter=';',
#                         usecols=['DateTime',
#                                  'Machine',
#                                  'Boxes',
#                                  ],
#                         )
# df_previous = pd.read_csv('./raw_data/boxes_total_previous.csv',
#                          delimiter=';',
#                          usecols=['DateTime',
#                                   'Machine',
#                                   'Boxes',
#                                   ],
#                          )

# Read in all the CSV files
cm_time = pd.read_csv("./raw_data/Corrective Maintenance Time.csv",
                      delimiter=';',
                      usecols=['DateTime',
                               'Machine',
                               'Time',
                               ],
                      )
et_time = pd.read_csv("./raw_data/Error Time.csv",
                      delimiter=';',
                      usecols=['DateTime',
                               'Machine',
                               'Time',
                               ],
                      )
it_time = pd.read_csv("./raw_data/Idle Time.csv",
                      delimiter=';',
                      usecols=['DateTime',
                               'Machine',
                               'Time',
                               ],
                      )
pm_time = pd.read_csv("./raw_data/Preventive Maintenance Time.csv",
                      delimiter=';',
                      usecols=['DateTime',
                               'Machine',
                               'Time',
                               ],
                      )
rt_time = pd.read_csv("./raw_data/Run Time.csv",
                      delimiter=';',
                      usecols=['DateTime',
                               'Machine',
                               'Time',
                               ],
                      )

# Merge all the dataframes on 'Machine' and 'DateTime'
df_time_merged = pd.merge(cm_time,
                          et_time,
                          on=["Machine",
                              "DateTime",],
                          how="outer",
                          )
df_time_merged = pd.merge(df_time_merged,
                          it_time,
                          on=["Machine",
                              "DateTime",],
                          how="outer",
                          )
df_time_merged = pd.merge(df_time_merged,
                          pm_time,
                          on=["Machine",
                              "DateTime",],
                          how="outer",
                          )
df_time_merged = pd.merge(df_time_merged,
                          rt_time,
                          on=["Machine",
                              "DateTime",],
                          how="outer",
                          )

# Replace missing values with 0
df_time_merged.fillna(0,
                      inplace=True,
                      )

print(df_time_merged)
# -----------------------------------------------------------------------------

# start of figuremaking
# -----------------------------------------------------------------------------

# Plot total Boxes Year over Year
# -----------------------------------------------------------------------------
fig_byoy = ig.plot_boxes_by_month(
    df_current,
    df_previous,
    machine_names,
    start_date,
    end_date,
)

plt.show(fig_byoy)

# TODO: save plot as pdf to use it in the report
# -----------------------------------------------------------------------------
