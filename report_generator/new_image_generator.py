# The image generator contains all functions that are
# used to create the various plots used in the
# monthly Packing Machine Report. Data is supplied
# by the Report Generator.
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
import matplotlib.dates as mdates
import matplotlib.lines as mlines
import matplotlib.ticker as mtick
import matplotlib.patches as mpatches
import new_calculator as nc
from matplotlib.lines import Line2D
# -----------------------------------------------------------------------------

# set global plt parameters
# -----------------------------------------------------------------------------
plt.rcParams['figure.figsize'] = [16.0, 9.0]  # [16.0, 9.0]
plt.rcParams['figure.dpi'] = 100
plt.rcParams['font.family'] = 'Europa-Regular'
plt.rcParams['axes.grid'] = True
plt.rcParams['axes.grid.axis'] = 'y'
plt.rcParams['axes.axisbelow'] = True
plt.rcParams['legend.frameon'] = False
plt.rcParams['legend.loc'] = 'upper center'
plt.rcParams['lines.linewidth'] = 3.5
plt.rcParams['font.size'] = 16
plt.rcParams['axes.spines.left'] = False
plt.rcParams['axes.spines.bottom'] = False
plt.rcParams['axes.spines.top'] = False
plt.rcParams['axes.spines.right'] = False
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
                Line2D([0], [0], color=palette_lc(4), lw=8)
                ]
# -----------------------------------------------------------------------------


# Plot total Boxes Year over Year
# -----------------------------------------------------------------------------
def plot_boxes_by_month(df_current_orig, machine_names, start_date, end_date, title='', df_previous_orig=None):
    """
     Plot the comparison of boxes by month for two dataframes containing the number of boxes for different machines.

    Args:
        df_current (pandas.DataFrame): A dataframe containing the current boxes data for the machines.
        df_previous (pandas.DataFrame, optional): A dataframe containing the previous year boxes data for the machines. Defaults to None.
        machine_names (list): A list of machine names to be plotted.
        start_date (datetime): A datetime object representing the start date of the desired time period.
        end_date (datetime): A datetime object representing the end date of the desired time period.

    Returns:
        matplotlib.figure.Figure: A grouped bar chart comparing the number of boxes for each month and year.
    """
    df_current = df_current_orig.copy()
    if df_previous_orig is not None:
        df_previous = df_previous_orig.copy()
    else:
        df_previous = None

    # Ensure start_date and end_date are datetime objects
    if isinstance(start_date, str):
        start_date = pd.to_datetime(start_date)
    if isinstance(end_date, str):
        end_date = pd.to_datetime(end_date)

    # Filter rows where 'Machine' is in the list of Machine Names
    df_current = df_current[df_current['Machine'].isin(machine_names)]
    # Convert DateTime column to pandas datetime format
    df_current['DateTime'] = pd.to_datetime(df_current['DateTime'])

    if df_previous is not None:
        df_previous = df_previous[df_previous['Machine'].isin(machine_names)]
        df_previous['DateTime'] = pd.to_datetime(df_previous['DateTime'])
        df_previous['DateTime'] = df_previous['DateTime'] + \
            pd.offsets.DateOffset(years=1)
        df_merged = pd.merge(df_current, df_previous,
                             on='DateTime', how='outer')

        # Rename the columns to differentiate between the two sets of boxes
        df_merged = df_merged.rename(
            columns={'Boxes_x': 'Boxes_current', 'Boxes_y': 'Boxes_previous'})
    else:
        df_merged = df_current.rename(columns={'Boxes': 'Boxes_current'})

    # Extract the values for the desired time period
    df_period = df_merged[(df_merged['DateTime'] >= start_date) & (
        df_merged['DateTime'] < end_date)]

    # Group by month and year and sum Boxes values for each month and year
    df_period_monthly = df_period.groupby(
        pd.Grouper(key='DateTime', freq='M')).sum()

    # Create a grouped bar chart comparing the boxes in each month
    labels = df_period_monthly.index.strftime('%b')
    x = np.arange(len(labels))
    width = 0.35  # the width of the bars

    fig, ax = plt.subplots()

    if df_previous is not None:
        rects1 = ax.bar(
            x - width/2, df_period_monthly['Boxes_previous'], width, label='Previous', color=palette_list[5])
        rects2 = ax.bar(
            x + width/2, df_period_monthly['Boxes_current'], width, label='Current', color=palette_list[4])
        rects = rects1 + rects2
        # Add y-axis label and legend
        ax.set_ylabel('Boxes')
        ax.legend()
    else:
        rects = ax.bar(
            x, df_period_monthly['Boxes_current'], width, color=palette_list[4])
        ax.set_ylabel('Boxes')

    # Add text labels to each column
    for rect in rects:
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width() / 2, height,
                int(height), ha='center', va='bottom', fontsize=16)

    # Set tick labels and title
    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=45, ha='right')
    ax.set_xlabel("")
    ax.set_title(title)

    return fig
# -----------------------------------------------------------------------------


# Make a donut Chart with all Machines and plot the total in the middle
# -----------------------------------------------------------------------------
def create_donut_chart(df_donut_orig, machine_names, title=''):
    df_donut = df_donut_orig.copy()
    # Filter the rows to include only the last available month
    df_donut['DateTime'] = pd.to_datetime(
        df_donut['DateTime'], format='%Y/%m')
    last_month = df_donut['DateTime'].max()
    df_last_month = df_donut[df_donut['DateTime'] == last_month]

    # Filter the rows to include only the desired machines
    df_machines = df_last_month[df_last_month['Machine'].isin(machine_names)]

    # Calculate the total number of boxes for the selected machines
    total_boxes = df_machines['Boxes'].sum()

    # Create labels with absolute values
    labels = [f"{value}" for value in df_machines['Boxes']]

    # Create a pie chart with the selected machines
    colors = [c for c in palette_list if c != 'grey']
    fig, ax = plt.subplots()
    wedges, texts = ax.pie(df_machines['Boxes'],
                           labels=labels,
                           colors=colors,
                           startangle=90,
                           textprops={'fontsize': 16},
                           wedgeprops={'linewidth': 7, 'edgecolor': 'white'}
                           )
    center_circle = plt.Circle((0, 0),
                               0.5,
                               color='white',
                               )
    fig = plt.gcf()
    fig.gca().add_artist(center_circle)

    # Format labels and texts
    plt.setp(texts, size=16)

    # Add the total number of boxes to the center of the chart
    ax.text(0,
            0,
            total_boxes,
            ha='center',
            va='center',
            fontsize=16,
            )

    # Create legend
    box = ax.get_position()
    ax.set_position([box.x0, box.y0 + box.height * 0.2,
                     box.width, box.height * 0.8,
                     ])
    ax.legend(custom_lines,
              machine_names,
              bbox_to_anchor=(0.5, -0.15),
              ncol=4,
              )
    # Set the title of the chart
    # ax.set_title(
    #    title + ' ({})'.format(last_month.strftime('%b %Y')), fontsize=20)

    # set axis equal to ensure circle is drawn as a circle
    plt.axis('equal')

    return fig
# -----------------------------------------------------------------------------


# create a single line chart that shows the total daily produced boxes
# -----------------------------------------------------------------------------
def create_single_lineplot(df_orig, machine_names, x_col, y_col, title=''):
    """
    Creates a line plot of box values for a specific machine for each day
    of the month.

    Args:
    - df (pd.DataFrame): the dataframe containing the data to plot
    - machine_names (str): the name of the machine to plot data for
    - x_col (str): name of the column to be used for the x-axis
    - y_col (str): name of the column to be used for the y-axis
    - title (str): title of the plot

    Returns:
    - matplotlib.figure.Figure: the resulting figure
    """
    df = df_orig.copy()
    # format DateTime to dd/mm
    df['DateTime'] = pd.to_datetime(df[x_col])
    # df['DateTime'] = df['DateTime'].dt.strftime('%d/%m')

    # filter for the specified machine
    machine_df = df[df['Machine'] == machine_names]

    # create the line plot, move the legend to the bottom
    fig, ax = plt.subplots()
    machine_df.plot(x='DateTime', y=y_col, color=palette_list[4], ax=ax)
    box = ax.get_position()
    ax.set_position([box.x0, box.y0 + box.height * 0.2,
                     box.width, box.height * 0.8,
                     ],
                    )
    ax.legend([machine_names],
              bbox_to_anchor=(0.5, -0.15),
              ncol=1,
              )
    plt.box(False)
    plt.xticks(rotation=45)

    # set x-ticks for every date
    ax.xaxis.set_major_locator(mdates.DayLocator())

    ax.xaxis.set_major_formatter(mdates.DateFormatter(
        '%d/%m'))  # format x-ticks as 'dd/mm'

    ax.grid(axis='x')  # This will only enable gridlines for x-axis
    ax.set_xlabel("")

    return fig
# -----------------------------------------------------------------------------


# create a grouped barplot showing daily produced boxes per machine
# -----------------------------------------------------------------------------
def create_grouped_barplot(df_barplot_orig, machine_names, x_col, y_col, title=''):
    """
    Create a grouped barplot with the total number of boxes for a given set of machines.

    Args:
        df_barplot (pd.DataFrame): A pandas DataFrame containing the data to be plotted.
        machine_names (List[str]): A list of strings representing the names of the machines to be included in the chart.
        x_col (str): name of the column to be used for the x-axis.
        y_col (str): name of the column to be used for the y-axis.
        title (str): A string with the title of the chart.

    Returns:
        plt.Figure: A matplotlib Figure object containing the resulting grouped bar plot.

    Example:
        Create a grouped barplot for machines A and B:

        >>> df_barplot = pd.read_csv('data.csv')
        >>> create_grouped_barplot(df_barplot, ['Machine A', 'Machine B'], 'DateTime', 'Boxes', 'Total Boxes for Machines A and B')
    """
    # Make a copy of the DataFrame
    df_barplot = df_barplot_orig.copy()

    # Format DateTime to dd/mm
    df_barplot[x_col] = pd.to_datetime(df_barplot[x_col])
    df_barplot[x_col] = df_barplot[x_col].dt.strftime('%d/%m')

    # Convert y_col values to numeric if applicable
    df_barplot = nc.percentage_to_float(df_barplot, y_col)

    # Create grouped barplot with legend at bottom
    fig, ax = plt.subplots()
    sns.barplot(x=x_col,
                y=y_col,
                hue='Machine',
                palette=palette_list,
                data=df_barplot[df_barplot['Machine'].isin(machine_names)],
                ax=ax,
                )
    box = ax.get_position()
    ax.set_position([box.x0, box.y0 + box.height * 0.2,
                     box.width, box.height * 0.8,
                     ])
    ax.legend(custom_lines,
              machine_names,
              bbox_to_anchor=(0.5, -0.15),
              ncol=4,
              )
    ax.set_xlabel("")
    plt.box(False)
    plt.xticks(rotation=45)

    # return the figure
    return fig
# -----------------------------------------------------------------------------


# create a multiline plot that shows each machine in a subplot
# -----------------------------------------------------------------------------
def create_multi_lineplot(df_lineplot_orig, machine_names, x_col, y_col, title=''):
    """
    Create a set of line plots showing the box counts over time for each machine.

    Args:
        df (pd.DataFrame): A pandas DataFrame containing the data to be plotted.
        machine_names (List[str]): A list of strings representing the names of the machines to be included in the chart.
        palette_list (List[str]): A list of color codes to be used for each machine.
        title (str): A string with the title of the chart.
        x_col (str): The name of the DataFrame column to use for the x-axis.
        y_col (str): The name of the DataFrame column to use for the y-axis.

    Returns:
        plt.Figure: A matplotlib Figure object containing the resulting line plots.

    Example:
        Create a grouped barplot for machines A and B:

        >>> df_lineplot = pd.read_csv('data.csv')
        >>> create_lineplot(df_barplot, ['Machine A', 'Machine B'], 'Total Boxes for Machines A and B')
    """

    # format DateTime to dd/mm
    df_lineplot = df_lineplot_orig.copy()
    df_lineplot['DateTime'] = pd.to_datetime(df_lineplot['DateTime'])
    df_lineplot['DateTime'] = df_lineplot['DateTime'].dt.strftime('%d/%m')

    # Create a list of subplots
    fig, axs = plt.subplots(2, 2, figsize=(16, 9), sharey=True)

    # Flatten the axs array to allow for easier iteration
    axs = axs.flatten()

    # Create a locator object to choose nice date ticks
    locator = mdates.AutoDateLocator()

    # Iterate over each subplot
    for i, ax in enumerate(axs):
        for i, machine in enumerate(machine_names):
            # Create a filtered dataframe for the current machine
            curr_df = df_lineplot[df_lineplot["Machine"] == machine]

            # Create a line plot for the current machine and other machines
            for machine_bg in machine_names:
                curr_df_bg = df_lineplot[df_lineplot["Machine"] == machine_bg]
                # Plot other machine's lines in light gray
                axs[i].plot(curr_df_bg[x_col], curr_df_bg[y_col],
                            color="lightgrey", linewidth=1, zorder=1)

            # Plot the current machine's line in color and with higher zorder
            axs[i].plot(curr_df[x_col], curr_df[y_col],
                        color=palette_list[i], linewidth=2, zorder=2)

            # Set the title for the current subplot
            ax.set_title(machine_names[i], fontsize=14)

            # Set the x-axis locator
            ax.xaxis.set_major_locator(locator)

            # Rotate the x-axis labels for readability
            ax.tick_params(axis="x", rotation=45)

    # Set the y-axis label for the entire figure
    fig.text(0.04, 0.5, "Boxes", va="center", rotation="vertical")

    # Set the overall title for the entire figure
    # fig.suptitle("Box counts by machine", fontsize=16)

    # Adjust the layout of the subplots to improve readability
    plt.subplots_adjust(wspace=0.05, hspace=0.3)

    return fig
# -----------------------------------------------------------------------------


# create a 2x2 barplot to show stuff by day and machine.
# -----------------------------------------------------------------------------
def create_multi_barplot(df_mbp_orig, machine_names, x_col=None, y_col=None, title=''):
    """
    Create a grouped bar plot for a given set of machines.

    Args:
        df_mbp_orig (pd.DataFrame): The original DataFrame containing the data to be plotted.
        machine_names (List[str]): A list of strings representing the names of the machines to be included in the chart.
        x_col (str): The name of the column to be used for the x-axis. Default is 'DateTime'.
        y_col (str): The name of the column to be used for the y-axis. Default is 'Boxes'.
        title (str): The title of the chart.

    Returns:
        plt.Figure: A matplotlib Figure object containing the resulting grouped bar plot.
    """
    if x_col is None:
        x_col = "DateTime"
    if y_col is None:
        y_col = "Boxes"

    # Create a copy of the original DataFrame
    df_mbp = df_mbp_orig.copy()

    # Format DateTime column to month abbreviation
    df_mbp['DateTime'] = pd.to_datetime(df_mbp[x_col])
    df_mbp['DateTime'] = df_mbp[x_col].dt.strftime('%b')

    # Check if y_col values are strings and if they are percentages (strings ending with '%')
    if df_mbp[y_col].dtype == 'object':
        is_percentage = df_mbp[y_col].str.endswith('%').any()
    else:
        is_percentage = False

    if is_percentage:
        # Convert y_col values to numeric
        df_mbp[y_col] = df_mbp[y_col].str.rstrip('%').astype(float) / 100

    # Create the subplots
    fig, axs = plt.subplots(2, 2, figsize=(16, 9), sharey=True)
    axs = axs.flatten()

    # Choose nice date ticks
    locator = mdates.AutoDateLocator()

    # Iterate over each machine name and corresponding color
    for i, (machine, color) in enumerate(zip(machine_names, palette_list)):
        # Filter the DataFrame for the current machine
        curr_df = df_mbp[df_mbp["Machine"] == machine]

        # Plot the bars
        axs[i].bar(curr_df[x_col], curr_df[y_col], color=color, linewidth=2)

        # Add value labels on top of each bar
        rects = axs[i].bar(curr_df[x_col], curr_df[y_col],
                           color=color, linewidth=2)
        for rect in rects:
            height = rect.get_height()
            if is_percentage:
                # Format as percentage if is_percentage is True
                label = f'{height:.2f}'
            else:
                # Format as integer if height is a whole number, or as a float otherwise
                label = f'{int(height)}' if height.is_integer(
                ) else f'{height:.2f}'
            axs[i].text(rect.get_x() + rect.get_width() / 2., height + 0.01, label,
                        ha='center', va='bottom', fontsize=14)

        # Set y-axis scaling and format y-axis labels as percentages if applicable
        max_y_value = df_mbp[y_col].max()
        if is_percentage:
            y_limit = (max_y_value // 0.1 + 1) * 0.1  # Round up to nearest 10%
            plt.ylim(0, y_limit)
            axs[i].yaxis.set_major_formatter(mtick.PercentFormatter(xmax=1))

        # Set title, x-axis locator, and x-axis rotation for the subplot
        axs[i].set_title(machine, fontsize=14)
        axs[i].xaxis.set_major_locator(locator)
        axs[i].tick_params(axis="x", rotation=45)

    # Set y-axis label for the entire figure
    fig.text(0.04, 0.5, y_col, va="center", rotation="vertical")

    # Adjust the layout of the subplots
    plt.subplots_adjust(wspace=0.05, hspace=0.3)

    return fig
# -----------------------------------------------------------------------------

# create a piechart of different machine states


def create_pie_chart(df_pie_orig, machine_name, total_seconds, title=''):

    # Define the labels for the pie chart slices
    labels = ['Run', 'Idle', 'Error', 'Prev', 'Corr', 'Undefined']

    df_pie = df_pie_orig.copy()
    time_cols = ["Hours_run_time", "Hours_idle_time", "Hours_error",
                 "Hours_prev_maint", "Hours_corr_maint", ]

    if machine_name == "Total":
        df_pie = df_pie[df_pie["Machine"] == machine_name]
        total_seconds *= 4
    else:
        df_pie = df_pie[df_pie["Machine"] == machine_name]
        title = machine_name

    time_totals = {}
    for col in time_cols:
        time_totals[col] = nc.convert_to_seconds(df_pie[col])

    # Calculate "run time" as "run time" minus "idle time"
    time_totals['Hours_run_time'] -= time_totals['Hours_idle_time']

    # Calculate "undefined" time as "total time" minus all the other times
    time_totals['undefined'] = total_seconds - sum(time_totals.values())

    # Create the pie chart
    fig, ax = plt.subplots()
    ax.pie(time_totals.values(), labels=labels,
           colors=palette_list, autopct='%1.1f%%',
           pctdistance=0.85, startangle=0)

    # Create legend items
    legend_items = [mpatches.Patch(color=color, label=label)
                    for color, label in zip(palette_list, labels)]

    box = ax.get_position()
    ax.set_position([box.x0, box.y0 + box.height * 0.2,
                     box.width, box.height * 0.8,
                     ])
    ax.legend(handles=legend_items,
              bbox_to_anchor=(0.5, -0.15),
              ncol=3,
              )
    ax.set_xlabel("")
    plt.box(False)
    plt.xticks(rotation=45)

    # Set the title
    plt.title(title)
    return fig
