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
import os
import subprocess
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.colors as colors
import seaborn as sns
import new_image_generator as ig
import get_data_from_dashboard as gdfd
import download_data as dd
import read_data_from_csv as rdfc
import new_calculator as nc
from getpass import getpass
from matplotlib.lines import Line2D
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
# -----------------------------------------------------------------------------

# set machine_names
# -----------------------------------------------------------------------------
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
historic_start_date = end_date - relativedelta(months=11)
historic_start_date = historic_start_date.replace(day=1)

# Format start_date and end_date as strings
start_date_str = start_date.strftime("%d/%m/%Y")
historic_start_date_str = historic_start_date.strftime("%d/%m/%Y")
end_date_str = end_date.strftime("%d/%m/%Y")

# calcualte total second available between the two given dates
working_seconds = nc.calculate_total_seconds_worked(start_date, end_date)
print(working_seconds)

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

# download the data
# -----------------------------------------------------------------------------
dd.download_data_parts(driver,
                       start_date_str,
                       end_date_str,
                       historic_start_date_str,
                       )
# -----------------------------------------------------------------------------


# Read in all the CSV files and create dataframes
# -----------------------------------------------------------------------------
df_time = rdfc.merge_time_data()
df_monthly = rdfc.merge_monthly_data()
df_historical = rdfc.merge_historical_data()
# -----------------------------------------------------------------------------

# create figures and save them to the output folder
# -----------------------------------------------------------------------------
output = ig.create_single_lineplot(
    df_monthly, 'Total', 'DateTime', 'Boxes')
plt.savefig('./output/img/lineplot_daily_boxes.pdf')
plt.clf()

output = ig.create_grouped_barplot(
    df_monthly, machine_names, 'DateTime', 'Boxes')
plt.savefig('./output/img/groupedbar_daily_boxes.pdf')
plt.clf()

output = ig.create_donut_chart(df_historical, machine_names,)
plt.savefig('./output/img/donut_total_boxes.pdf')
plt.clf()

output = ig.plot_boxes_by_month(df_historical, machine_names,
                                historic_start_date, end_date,)
plt.savefig('./output/img/barplot_monthly_boxes.pdf')
plt.clf()

output = ig.create_multi_lineplot(
    df_monthly, machine_names, 'DateTime', 'machine_tp')
plt.savefig('./output/img/multiline_daily_tp.pdf')
plt.clf()

output = ig.create_multi_barplot(
    df_historical, machine_names, 'DateTime', 'machine_tp')
plt.savefig('./output/img/multibar_monthly_tp.pdf')
plt.clf()

output = ig.create_multi_lineplot(
    df_monthly, machine_names, 'DateTime', 'machine_tp_cmc')
plt.savefig('./output/img/multiline_daily_tp_cmc.pdf')
plt.clf()

output = ig.create_multi_barplot(
    df_historical, machine_names, 'DateTime', 'machine_tp_cmc')
plt.savefig('./output/img/multibar_monthly_tp_cmc.pdf')
plt.clf()

output = ig.create_single_lineplot(
    df_monthly, 'Total', 'DateTime', 'abs_bad_boxes')
plt.savefig('./output/img/lineplot_daily_abs_bad_boxes.pdf')
plt.clf()

output = ig.create_grouped_barplot(
    df_monthly, machine_names, 'DateTime', 'abs_bad_boxes')
plt.savefig('./output/img/groupedbar_daily_abs_bad_boxes.pdf')
plt.clf()

output = ig.create_grouped_barplot(
    df_monthly, machine_names, 'DateTime', 'rel_bad_boxes')
plt.savefig('./output/img/groupedbar_daily_rel_bad_boxes.pdf')
plt.clf()

output = ig.create_multi_barplot(
    df_historical, machine_names, 'DateTime', 'rel_bad_boxes')
plt.savefig('./output/img/multibar_monthly_rel_bad_boxes.pdf')
plt.clf()

output = ig.create_grouped_barplot(
    df_monthly, machine_names, 'DateTime', 'op_avail')
plt.savefig('./output/img/groupedbar_daily_op_avail.pdf')
plt.clf()

output = ig.create_multi_barplot(
    df_historical, machine_names, 'DateTime', 'op_avail')
plt.savefig('./output/img/multibar_monthly_op_avail.pdf')
plt.clf()

print(df_historical)
output = ig.create_multi_barplot(
    df_historical, machine_names, 'DateTime', 'carton_per_box')
plt.savefig('./output/img/multibar_monthly_carton_per_box.pdf')
plt.clf()

# create these plots last to not cause errors in other functions
machine_names.append('Total')
#
for machine_name in machine_names:
    output = ig.create_pie_chart(df_time, machine_name, working_seconds)
    plt.savefig('./output/img/piechart_monthly_' + machine_name + '.pdf')
    plt.clf()

os.chdir(os.getcwd() + '/output')
# call lualatex and compile the texfile
subprocess.check_call(['lualatex', 'monthly_report.tex'])
# -----------------------------------------------------------------------------
