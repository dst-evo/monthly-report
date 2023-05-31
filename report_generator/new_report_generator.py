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
import download_data as dd
import read_data_from_csv as rdfc
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

# TODO: input() instead of hardcoded if necessary
ip_address = "172.22.139.212"
# -----------------------------------------------------------------------------


# download all needed data
# -----------------------------------------------------------------------------
# configure driver
# print("Configuring Selenium webdriver")
# driver = gdfd.create_configured_driver(ip_address)
#
# login into the dasboard
# print("Starting the login process")
# gdfd.login(driver, username, password)

# download the data
# -----------------------------------------------------------------------------
# dd.download_data_parts(driver,
#                       start_date_str,
#                       end_date_str,
#                       second_start_date_str,
#                       )
# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
# Read in all the CSV files
df_time = rdfc.merge_time_data()
#df_monthly = rdfc.merge_monthly_data()
df_historical = rdfc.merge_historical_data()

#
output = ig.plot_boxes_by_month(df_historical, machine_names,
                       historic_start_date, end_date, 'Total Boxes per Month')

plt.show()
# -----------------------------------------------------------------------------
