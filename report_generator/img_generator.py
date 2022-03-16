from turtle import color
from typing import ValuesView
from matplotlib import rcParams
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.dates as mdates
from matplotlib.dates import DateFormatter
import numpy as np
import pandas as pd
import datetime as dt

# viridis discrete hex codes
#   #FDE725 = L1 - VPM B (4958)
#   #7AD151 = L2 - VPM A (4959)
#   #22A884 = L3 - VPM C (4960)
#   #2A788E = L4 - VPM D (4961)
#   #414487 = Totals

# set global parameters
plt.rcParams['figure.figsize'] = [16.0, 9.0]
plt.rcParams['figure.dpi'] = 300
plt.rcParams['font.family'] = 'Europa-Regular'
plt.rcParams['axes.grid'] = True
plt.rcParams['axes.grid.axis'] = 'y'
plt.rcParams['axes.axisbelow'] = True
plt.rcParams['legend.frameon'] = False
plt.rcParams['legend.loc'] = 'upper center'
plt.rcParams['lines.linewidth'] = 3.5

# print a single linechart
# this is used for the following values:
#   total produced boxes per day
#   bad boxes per day


def single_linechart(val_b, val_a, val_c, val_d, date):
    x = np.arange(len(date))

    fig, ax = plt.subplots()
    values = val_a + val_b.values + val_c.values + val_d.values
    ax.plot(values, color='#414487')

    ax.set_ylabel('Packages')
    ax.set_ylim(bottom=0, top=35000)
    box = ax.get_position()
    ax.set_position([box.x0, box.y0 + box.height *
                    0.1, box.width, box.height * 0.9])
    ax.legend(['Total'], bbox_to_anchor=(0.5, -0.05), ncol=1)

    day_locator = mdates.DayLocator()
    day_month_formatter = mdates.DateFormatter(
        "%d/%m")  # four digits for year, two for month
    ax.xaxis.set_major_locator(day_locator)
    # ax.xaxis.set_major_locator(mdates.AutoDateLocator())
    # formatter for major axis only
    ax.xaxis.set_major_formatter(day_month_formatter)

    fig.tight_layout()
    fig.autofmt_xdate()

    plt.box(False)
    plt.xticks(rotation=45)

    # save plot
    plt.savefig('./output/img/single_linechart.svg')


# barplot to display daily values for each machine
# this is used for the following values:
#   total produced boxes per day and machine
#   absolut bad boxes per day and machine
#   relative bad boxes per day and machine
def daily_barplot(val_b, val_a, val_c, val_d, date):
    x = np.arange(len(date))
    barWidth = 0.2

    fig, ax = plt.subplots()
    bar_b = ax.bar(x-(barWidth*1.5), val_b, width=barWidth, label='L1 - VPM B (4958)',
                   color='#FDE725')
    bar_a = ax.bar(x-(barWidth*0.5), val_a, width=barWidth, label='L2 - VPM A (4959)',
                   color='#7AD151')
    bar_c = ax.bar(x+(barWidth*0.5), val_c, width=barWidth, label='L3 - VPM C (4960)',
                   color='#22A884')
    bar_d = ax.bar(x+(barWidth*1.5), val_d, width=barWidth, label='L4 - VPM D (4961)',
                   color='#2A788E')

    ax.set_ylabel('Packages')
    # ax.set_title('Daily Packages per Machine')
    ax.set_ylim(bottom=0, top=10000)

    box = ax.get_position()
    ax.set_position([box.x0, box.y0 + box.height *
                    0.1, box.width, box.height * 0.9])
    ax.legend(bbox_to_anchor=(0.5, -0.05), ncol=5)

    ax.set_xticks(range(date.size))
    ax.set_xticklabels([ts.strftime('%d/%m') if ts.year != date[idx-1].year
                        else ts.strftime('%d/%m') for idx, ts in enumerate(date)])

    fig.tight_layout()
    fig.autofmt_xdate()

    plt.box(False)
    plt.xticks(rotation=45)
    plt.savefig('./output/img/daily_barplot.svg')

# barplot to display monthly averages for each machine
# this is used for the following values:
#   average produced boxes per hour per machine
#   average produced boxes per hour per machine - CMC
#   average relative boxes per machine
#   average availability


def monthly_barplot():
    # Make a random dataset:
    height = [3, 12, 5, 18, 45]
    bars = ('A', 'B', 'C', 'D', 'E')
    y_pos = np.arange(len(bars))

    # Create bars
    plt.bar(y_pos, height)

    # Create names on the x-axis
    plt.xticks(y_pos, bars)

    # Show graphic
    plt.savefig('./output/img/monthly_barplot.png')
