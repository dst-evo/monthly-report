from turtle import color
from typing import ValuesView
from cv2 import rotate
from matplotlib import rcParams
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.dates as mdates
from matplotlib.dates import DateFormatter
import numpy as np
import pandas as pd
import datetime as dt

import calculations

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

# set color palette
palette = plt.get_cmap('viridis', 5)

# print a single linechart
# this is used for the following values:
#   total produced boxes per day
#   bad boxes per day


def single_linechart(val_b, val_a, val_c, val_d, date, tag):
    x = np.arange(len(date))

    fig, ax = plt.subplots()
    values = val_a.values + val_b.values + val_c.values + val_d.values
    ax.plot(values, color=palette(0))

    ax.set_ylim(bottom=0, top=40000)

    box = ax.get_position()
    ax.set_position([box.x0, box.y0 + box.height *
                    0.1, box.width, box.height * 0.9])
    ax.legend(['Total'], bbox_to_anchor=(0.5, -0.05), ncol=1)

    ax.set_xticks(range(date.size))
    ax.set_xticklabels([ts.strftime('%d/%m') if ts.year != date[idx-1].year
                        else ts.strftime('%d/%m') for idx, ts in enumerate(date)])

    fig.tight_layout()
    fig.autofmt_xdate()

    plt.box(False)
    plt.xticks(rotation=45)

    # save plot
    plt.savefig('./output/img/single_linechart_' + tag + '.svg')

# barplot to display daily values for each machine
# this is used for the following values:
#   total produced boxes per day and machine
#   absolut bad boxes per day and machine
#   relative bad boxes per day and machine


def daily_barplot(val_b, val_a, val_c, val_d, date, tag):
    x = np.arange(len(date))
    barWidth = 0.2

    fig, ax = plt.subplots()
    ax.bar(x-(barWidth*1.5), val_b, width=barWidth, label='L1 - VPM B (4958)',
           color=palette(4))
    ax.bar(x-(barWidth*0.5), val_a, width=barWidth, label='L2 - VPM A (4959)',
           color=palette(3))
    ax.bar(x+(barWidth*0.5), val_c, width=barWidth, label='L3 - VPM C (4960)',
           color=palette(2))
    ax.bar(x+(barWidth*1.5), val_d, width=barWidth, label='L4 - VPM D (4961)',
           color=palette(1))

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
    plt.savefig('./output/img/daily_barplot_' + tag + '.svg')

# barplot to display monthly averages for each machine
# this is used for the following values:
#   average produced boxes per hour per machine
#   average produced boxes per hour per machine - CMC
#   average relative boxes per machine
#   average availability


def multi_line(val_b, val_a, val_c, val_d, date, tag):
    df = pd.DataFrame({'date': date, 'L1 - VPM B (4958)': val_b.values, 'L2 - VPM A (4959)': val_a.values,
                      'L3 - VPM C (4960)': val_c.values, 'L4 - VPM D (4961)': val_d.values})

    # multiple line plot
    num = 0
    for column in df.drop('date', axis=1):
        num += 1

        # Find the right spot on the plot
        plt.subplot(2, 2, num)

        # plot every group, but discrete
        for v in df.drop('date', axis=1):
            plt.plot(df['date'], df[v], marker='',
                     color='grey', linewidth=0.6, alpha=0.3)

        # Plot the lineplot
        plt.plot(df['date'], df[column], marker='', color=palette(5-num),
                 label=column)

        # Same limits for every chart
        plt.ylim(0, 1000)

        # x-Ticks
        dtFmt = mdates.DateFormatter('%d/%m')
        plt.gca().xaxis.set_major_formatter(dtFmt)

        # Add title
        plt.title(column, loc='center', fontsize=12,
                  fontweight=0)

        plt.xticks(rotation=45)
        plt.tick_params(labelsize='8',)

        plt.tight_layout()
        plt.box(False)

    # Axis titles
    plt.text(0.5, 0.02, 'Time', ha='center', va='center')
    plt.text(0.06, 0.5, 'Note', ha='center', va='center', rotation='vertical')

    # Show the graph
    plt.savefig('./output/img/multiline_' + tag + '.svg')
