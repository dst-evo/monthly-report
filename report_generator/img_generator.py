import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


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
def daily_barplot(bars):
    # Make a random dataset:
    height = [3, 12, 5, 18, 45]
    #bars = ('A', 'B', 'C', 'D', 'E')
    y_pos = np.arange(len(bars))

    # Create bars
    plt.bar(y_pos, height)

    # Create names on the x-axis
    plt.xticks(y_pos, bars)

    # Show graphic
    plt.savefig('./output/img/daily_barplot.png')


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
