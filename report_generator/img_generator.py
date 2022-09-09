import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import pandas as pd
import matplotlib.colors as colors
from matplotlib.lines import Line2D
import matplotlib.ticker as mtick


import calculations

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
plt.rcParams['font.size'] = 22

# viridis discrete hex codes
#   #FDE725 = L1 - VPM B (4958)
#   #7AD151 = L2 - VPM A (4959)
#   #22A884 = L3 - VPM C (4960)
#   #2A788E = L4 - VPM D (4961)
#   #414487 = Totals

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
# print a single linechart
# this is used for the following values:
#   total produced boxes per day
#   bad boxes per day


def single_linechart(val_b, val_a, val_c, val_d, date, tag):
    x = np.arange(len(date))

    fig, ax = plt.subplots()
    values = val_a.values + val_b.values + val_c.values + val_d.values
    ax.plot(values, color=palette_lc(4))

    ax.set_ylim(bottom=0, top=max(values) + 0.1*max(values))

    box = ax.get_position()
    ax.set_position([box.x0, box.y0 + box.height *
                    0.2, box.width, box.height * 0.8])
    ax.legend(['Total'], bbox_to_anchor=(0.5, -0.15), ncol=1)

    ax.set_xticks(range(date.size))
    ax.set_xticklabels([ts.strftime('%d/%m') if ts.year != date[idx-1].year
                        else ts.strftime('%d/%m') for idx, ts in enumerate(date)])

    fig.tight_layout()
    fig.autofmt_xdate()

    plt.box(False)
    plt.xticks(rotation=45)

    # save plot
    plt.savefig('./output/img/single_linechart_' + tag + '.pdf')
    plt.clf()

# barplot to display daily values for each machine
# this is used for the following values:
#   total produced boxes per day and machine
#   absolut bad boxes per day and machine
#   relative bad boxes per day and machine


def historic_single_barplot(values, tag):
    y_pos = np.arange(len(values))
    plt.bar(y_pos, values, color=palette_list[4])
    plt.gca().set_xticks(range(values.index.size))
    plt.gca().set_xticklabels([ts.strftime('%b') if ts.year != values.index[idx-1].year
                               else ts.strftime('%b') for idx, ts in enumerate(values.index)])
    add_value_labels(plt.gca())

    plt.tight_layout()
    # plt.autofmt_xdate()

    plt.box(False)
    plt.savefig('./output/img/historic_single_bar_' + tag + '.pdf')
    plt.clf()


def daily_barplot(val_b, val_a, val_c, val_d, date, tag, percentage=False, avail=True, isbb=False):
    x = np.arange(len(date))
    barWidth = 0.2
    fig, ax = plt.subplots()
    if percentage:
        ax.yaxis.set_major_formatter(mtick.PercentFormatter(1.0))
        if avail:
            ax.set_ylim(bottom=0, top=1.0)
        else:
            ax.set_ylim(bottom=0, top=0.1)
        val_b = val_b.str.rstrip('%').astype('float') / 100
        val_a = val_a.str.rstrip('%').astype('float') / 100
        val_c = val_c.str.rstrip('%').astype('float') / 100
        val_d = val_d.str.rstrip('%').astype('float') / 100

    else:
        if isbb:
            ax.set_ylim(bottom=0, top=600)
        else:
            ax.set_ylim(bottom=0, top=10000)
    ax.bar(x-(barWidth*1.5), val_b, width=barWidth, label='L1 - VPM B (4958)',
           color=palette_lc(0))
    ax.bar(x-(barWidth*0.5), val_a, width=barWidth, label='L2 - VPM A (4959)',
           color=palette_lc(1))
    ax.bar(x+(barWidth*0.5), val_c, width=barWidth, label='L3 - VPM C (4960)',
           color=palette_lc(2))
    ax.bar(x+(barWidth*1.5), val_d, width=barWidth, label='L4 - VPM D (4961)',
           color=palette_lc(3))

    box = ax.get_position()
    ax.set_position([box.x0, box.y0 + box.height *
                    0.2, box.width, box.height * 0.8])
    ax.legend(custom_lines, machine_names, bbox_to_anchor=(
        0.5, -0.15), ncol=len(machine_names))

    ax.set_xticks(range(date.size))
    ax.set_xticklabels([ts.strftime('%d/%m') if ts.year != date[idx-1].year
                        else ts.strftime('%d/%m') for idx, ts in enumerate(date)])

    fig.tight_layout()
    fig.autofmt_xdate()

    plt.box(False)
    plt.xticks(rotation=45, fontsize=20)
    plt.savefig('./output/img/daily_barplot_' + tag + '.pdf')
    plt.clf()

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

        # Find the right spot on the plot
        plt.subplot(2, 2, num+1)

        # plot every group, but discrete
        for v in df.drop('date', axis=1):
            plt.plot(df['date'], df[v], marker='',
                     color='grey', linewidth=0.6, alpha=0.3)

        # Plot the lineplot
        plt.plot(df['date'], df[column], marker='', color=palette_lc(num),
                 label=column)
        num += 1
        # Same limits for every chart
        plt.ylim(0, 1000)

        # x-Ticks
        dtFmt = mdates.DateFormatter('%d/%m')
        plt.gca().xaxis.set_major_formatter(dtFmt)

        # Add title
        plt.title(column, loc='center', fontsize=16,
                  fontweight=0)

        plt.xticks(rotation=45)
        plt.tick_params(labelsize='16',)

        plt.tight_layout()
        plt.box(False)

    # Axis titles
    plt.text(0.5, 0.02, 'Time', ha='center', va='center')
    plt.text(0.06, 0.5, 'Note', ha='center', va='center', rotation='vertical')

    # Save the plots
    plt.savefig('./output/img/multiline_' + tag + '.pdf')
    plt.clf()


def hisoric_multi(values, tag):
    y_pos = np.arange(len(values))
    num = 0
    for column in values:
        plt.subplot(2, 2, num+1)
        plt.bar(y_pos, values[column], color=palette_list[num])
        add_value_labels(plt.gca())

        plt.title(machine_names[num], loc='center', fontsize=16,
                  fontweight=0)

        plt.xticks()
        plt.tick_params(labelsize='16')

        plt.gca().set_xticks(range(values.index.size))
        plt.gca().set_xticklabels([ts.strftime('%b') if ts.year != values.index[idx-1].year
                                   else ts.strftime('%b') for idx, ts in enumerate(values.index)])

        plt.ylim(0, 750)

        plt.tight_layout()
        plt.box(False)
        num = num + 1

    plt.savefig('./output/img/historic_multi_' + tag + '.pdf')

    plt.clf()


def hisoric_multi_percent(values, tag='test', avail=False):
    y_pos = np.arange(len(values))
    num = 0
    y_max = []
    for column in values:
        plt.subplot(2, 2, num+1)
        plt.bar(y_pos, values[column], color=palette_list[num])
        add_value_labels(plt.gca(), True)

        plt.title(machine_names[num], loc='center', fontsize=16,
                  fontweight=0)

        plt.xticks()
        plt.tick_params(labelsize='16')

        plt.gca().set_xticks(range(values.index.size))
        plt.gca().set_xticklabels([ts.strftime('%b') if ts.year != values.index[idx-1].year
                                   else ts.strftime('%b') for idx, ts in enumerate(values.index)])
        plt.gca().yaxis.set_major_formatter(mtick.PercentFormatter(1.0))

        if avail:
            plt.ylim(0.0, 1.0)
        else:
            plt.ylim(0.0, 0.1)
        plt.tight_layout()
        plt.box(False)
        num = num + 1
    plt.savefig('./output/img/historic_multi_' + tag + '.pdf')

    plt.clf()


# pie chart to display relative time in different states

def pie_chart(values, tag):
    # create a list with total seconds for each machine state
    pie_vals = []
    names = []
    num = 0
    for x in values:
        if tag != 'Total':
            pie_vals.append(calculations.convert_to_seconds(values[x]))
        else:
            pie_vals.append(values.iloc[0][x])
        names.append(x)
    pie_vals[0] = pie_vals[0] - pie_vals[1]
    if tag != 'Total':
        pie_vals.append(calculations.get_ws_pm() - sum(pie_vals))
        names.append('undefined_time')

    for x in names:
        names[num] = x.split('_', 1)[0]
        names[num] = names[num].title()
        num = num + 1

    # Create a pieplot
    plt.pie(pie_vals, labeldistance=1.15, colors=palette_list,
            startangle=0, autopct='%1.0f%%', pctdistance=1.1, textprops={'fontsize': 22})
    plt.legend(names, loc="lower center",
               bbox_to_anchor=(0.5, -0.15), ncol=len(names))
    plt.title(tag)
    plt.tight_layout()
    # Show the graph

    plt.savefig('./output/img/pie_chart_' + tag + '.pdf')
    plt.clf()


def donut_chart(values, tag):
    # Create a pieplot
    plt.pie(values, labels=values, colors=palette_list, startangle=0, wedgeprops={
        'linewidth': 7, 'edgecolor': 'white'})

    # add a circle at the center to transform it in a donut chart
    my_circle = plt.Circle((0, 0), 0.7, color='white')
    p = plt.gcf()
    p.gca().add_artist(my_circle)
    plt.text(0, 0, sum(values), ha='center', va='center')
    plt.legend(custom_lines, machine_names, loc="lower center",
               bbox_to_anchor=(0.5, -0.15), ncol=len(machine_names))
    plt.tight_layout()

    plt.savefig('./output/img/donut_chart_' + tag + '.pdf')
    plt.clf()


# stolen from Stackoverflow https://stackoverflow.com/questions/28931224/adding-value-labels-on-a-matplotlib-bar-chart
def add_value_labels(ax, percent=False, spacing=5):
    """Add labels to the end of each bar in a bar chart.

    Arguments:
        ax (matplotlib.axes.Axes): The matplotlib object containing the axes
            of the plot to annotate.
        spacing (int): The distance between the labels and the bars.
    """

    # For each bar: Place a label
    for rect in ax.patches:
        # Get X and Y placement of label from rect.
        y_value = rect.get_height()
        x_value = rect.get_x() + rect.get_width() / 2

        # Number of points between bar and label. Change to your liking.
        space = spacing
        # Vertical alignment for positive values
        va = 'bottom'

        # If value of bar is negative: Place label below bar
        if y_value < 0:
            # Invert space to place label below
            space *= -1
            # Vertically align label at top
            va = 'top'

        # Use Y value as label and format number with one decimal place
        if percent:
            label = "{:.2%}".format(y_value)
        else:
            label = "{:.0f}".format(y_value)

        # Create annotation
        ax.annotate(
            label,                      # Use `label` as label
            (x_value, y_value),         # Place label at end of the bar
            xytext=(0, space),          # Vertically shift label by `space`
            textcoords="offset points",  # Interpret `xytext` as offset in points
            ha='center',                # Horizontally center label
            fontsize=16,
            va=va)                      # Vertically align label differently for
        # positive and negative values.
