from turtle import color
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import pandas as pd
import datetime as dt

# viridis discrete hex codes
#   #FDE725 = L1 - VPM B (4958)
#   #7AD151 = L2 - VPM A (4959)
#   #22A884 = L3 - VPM C (4960)
#   #2A788E = L4 - VPM D (4961)
#   #414487 = Totals
#
#

# print a single linechart
# this is used for the following values:
#   total produced boxes per day
#   bad boxes per day


def single_linechart():
    # create data
    values = np.cumsum(np.random.randn(1000, 1))

    # plot data
    plt.plot(values)

    # save plot
    plt.savefig('./output/img/single_linechart.png')


# barplot to display daily values for each machine
# this is used for the following values:
#   total produced boxes per day and machine
#   absolut bad boxes per day and machine
#   relative bad boxes per day and machine
def daily_barplot(height_b, height_a, height_c, height_d, date):
    barWidth = 0.25

    bar_b = np.arange(len(height_a))
    bar_a = [x + barWidth for x in bar_b]
    bar_c = [x + barWidth for x in bar_a]
    bar_d = [x + barWidth for x in bar_c]

    plt.bar(bar_b, height_b, width=barWidth, label='L1 - VPM B (4958)',
            color='#FDE725', edgecolor='white')
    plt.bar(bar_a, height_a, width=barWidth, label='L2 - VPM A (4959)',
            color='#7AD151', edgecolor='white')
    plt.bar(bar_c, height_c, width=barWidth, label='L3 - VPM C (4960)',
            color='#22A884', edgecolor='white')
    plt.bar(bar_d, height_d, width=barWidth, label='L4 - VPM D (4961)',
            color='#2A788E', edgecolor='white')

    plt.xlabel('date')
    plt.xticks([r + barWidth for r in range(len(height_a))], date)

    # save graphic

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
