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
import get_data_from_dashboard as gdfd
from getpass import getpass
from matplotlib.lines import Line2D
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
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

# configure login, dates and ip
# -----------------------------------------------------------------------------
# Get the username, password, and month from the user
username = input("Enter your username: ")
password = getpass("Enter your password: ")
year = int(input("Enter the year for the report: "))
month = int(input("Enter the month for the report (1-12): "))

# Calculate the start_date (first day of the month) and end_date (last day of the month)
start_date = datetime(year, month, 1)
if month == 12:
    end_date = datetime(year + 1, 1, 1) - timedelta(days=1)
else:
    end_date = datetime(year, month + 1, 1) - timedelta(days=1)

# Calculate the second start_date (12 months before the end_date)
second_start_date = end_date - relativedelta(months=11)
second_start_date = second_start_date.replace(day=1)

# Format start_date and end_date as strings
start_date_str = start_date.strftime("%d/%m/%Y")
second_start_date_str = second_start_date.strftime("%d/%m/%Y")
end_date_str = end_date.strftime("%d/%m/%Y")

# TODO: input() instead of hardcoded if necessary
ip_address = "172.22.139.212"
# -----------------------------------------------------------------------------


# download all needed data
# -----------------------------------------------------------------------------
# configure driver
print("Configuring Selenium webdriver")
driver = gdfd.create_configured_driver(ip_address)

# login into the dasboard
print("Starting the login process")
gdfd.login(driver, username, password)

# download data
print("Downloading Data part 1")
gdfd.configure_and_download_data(driver,
                                 "month",
                                 "yes",
                                 second_start_date_str,
                                 end_date_str,
                                 "Produced boxes",
                                 "boxes_total_current_interval.csv",
                                 )

print("Downloading Data part 2")
gdfd.configure_and_download_data(driver,
                                 "day",
                                 "no",
                                 start_date_str,
                                 end_date_str,
                                 "Produced boxes",
                                 "produced_boxes_daily.csv",
                                 )

print("Downloading Data part 3")
gdfd.configure_and_download_data(driver,
                                 "day",
                                 "no",
                                 start_date_str,
                                 end_date_str,
                                 "Throughput",
                                 "machine_tp.csv"
                                 )

print("Downloading Data part 4")
gdfd.configure_and_download_data(driver,
                                 "day",
                                 "no",
                                 start_date_str,
                                 end_date_str,
                                 "Throughput CMC",
                                 "machine_tp_cmc.csv"
                                 )

print("Downloading Data part 5")
gdfd.configure_and_download_data(driver,
                                 "day",
                                 "no",
                                 start_date_str,
                                 end_date_str,
                                 "Idle time",
                                 "idle_time.csv"
                                 )

print("Downloading Data part 6")
gdfd.configure_and_download_data(driver,
                                 "day",
                                 "no",
                                 start_date_str,
                                 end_date_str,
                                 "Run time",
                                 "run_time.csv"
                                 )

print("Downloading Data part 7")
gdfd.configure_and_download_data(driver,
                                 "day",
                                 "no",
                                 start_date_str,
                                 end_date_str,
                                 "Error time",
                                 "error_time.csv"
                                 )

print("Downloading Data part 8")
gdfd.configure_and_download_data(driver,
                                 "day",
                                 "no",
                                 start_date_str,
                                 end_date_str,
                                 "Corrective maintenance time",
                                 "corr_maint_time.csv"
                                 )

print("Downloading Data part 9")
gdfd.configure_and_download_data(driver,
                                 "day",
                                 "no",
                                 start_date_str,
                                 end_date_str,
                                 "Preventive maintenance time",
                                 "prev_maint_time.csv"
                                 )

print("Downloading Data part 9")
gdfd.configure_and_download_data(driver,
                                 "day",
                                 "no",
                                 start_date_str,
                                 end_date_str,
                                 "Bad boxes: All reasons",
                                 "bad_boxes.csv"
                                 )

print("Downloading Data part 10")
gdfd.configure_and_download_data(driver,
                                 "month",
                                 "no",
                                 second_start_date_str,
                                 end_date_str,
                                 "Bad boxes: All reasons",
                                 "bad_boxes_hist.csv"
                                 )

print("Downloading Data part 11")
gdfd.configure_and_download_data(driver,
                                 "month",
                                 "no",
                                 second_start_date_str,
                                 end_date_str,
                                 "Throughput",
                                 "machine_tp_hist.csv"
                                 )

print("Downloading Data part 12")
gdfd.configure_and_download_data(driver,
                                 "month",
                                 "no",
                                 second_start_date_str,
                                 end_date_str,
                                 "Throughput CMC",
                                 "machine_tp_cmc_hist.csv"
                                 )

print("Downloading Data part 13")
gdfd.configure_and_download_data(driver,
                                 "month",
                                 "no",
                                 second_start_date_str,
                                 end_date_str,
                                 "Operational availability",
                                 "op_avail_hist.csv"
                                 )

# -----------------------------------------------------------------------------
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
