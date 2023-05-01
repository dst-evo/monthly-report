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

machine_names = ['L1 - VPM B (4958)',
                 'L2 - VPM A (4959)',
                 'L3 - VPM C (4960)',
                 'L4 - VPM D (4961)',
                 ]

# define legend style
custom_lines = [Line2D([0], [0], color=palette_lc(0), lw=8),
                Line2D([0], [0], color=palette_lc(1), lw=8),
                Line2D([0], [0], color=palette_lc(2), lw=8),
                Line2D([0], [0], color=palette_lc(3), lw=8),
                ]
# -----------------------------------------------------------------------------


# Plot total Boxes Year over Year
# -----------------------------------------------------------------------------
def plot_boxes_by_month(df_current, df_previous, machine_names, start_date, end_date, title):
    """
     Plot the comparison of boxes by month for two dataframes containing the number of boxes for different machines.

    Args:
        df_current (pandas.DataFrame): A dataframe containing the current boxes data for the machines.
        df_previous (pandas.DataFrame): A dataframe containing the previous year boxes data for the machines.
        machine_names (list): A list of machine names to be plotted.
        start_date (datetime): A datetime object representing the start date of the desired time period.
        end_date (datetime): A datetime object representing the end date of the desired time period.

    Returns:
        matplotlib.figure.Figure: A grouped bar chart comparing the number of boxes for each month and year.
    """

    # Filter rows where 'Machine' is in the list of Machine Names
    df_current = df_current[df_current['Machine'].isin(machine_names)]
    df_previous = df_previous[df_previous['Machine'].isin(machine_names)]

    # Convert DateTime column to pandas datetime format
    df_current['DateTime'] = pd.to_datetime(df_current['DateTime'])
    df_previous['DateTime'] = pd.to_datetime(df_previous['DateTime'])

    # Add a year to the DateTime column in df_previous
    df_previous['DateTime'] = df_previous['DateTime'] + \
        pd.offsets.DateOffset(years=1)

    # Merge the two dataframes based on DateTime column
    df_merged = pd.merge(df_current, df_previous, on='DateTime')

    # Rename the columns to differentiate between the two sets of boxes
    df_merged = df_merged.rename(
        columns={'Boxes_x': 'Boxes_current', 'Boxes_y': 'Boxes_previous'})

    # Extract the values for the desired time period
    # start_date = pd.to_datetime('2022-04-01')
    # end_date = pd.to_datetime('2023-03-01')
    df_period = df_merged[(df_merged['DateTime'] >= start_date)
                          & (df_merged['DateTime'] < end_date)]

    # Group by month and year and sum Boxes values for each month and year
    df_period_monthly = df_period.groupby(
        pd.Grouper(key='DateTime', freq='M')).sum()

    # Create a grouped bar chart comparing the boxes in each month
    labels = df_period_monthly.index.strftime('%b')
    x = np.arange(len(labels))
    width = 0.35  # the width of the bars

    fig, ax = plt.subplots()
    # create the two bars
    rects1 = ax.bar(
        x - width/2,
        df_period_monthly['Boxes_previous'],
        width,
        color=palette_list[5],
        label='Previous',
    )
    rects2 = ax.bar(
        x + width/2,
        df_period_monthly['Boxes_current'],
        width,
        color=palette_list[4],
        label='Current',
    )
    # Add y-axis label and legend
    ax.set_ylabel('Boxes')
    box = ax.get_position()
    ax.set_position([box.x0,
                     box.y0 + box.height * 0.2,
                     box.width,
                     box.height * 0.8],
                    )
    ax.legend(['Previous', 'Current'],
              bbox_to_anchor=(0.5, -0.15),
              ncol=2,
              )

    # Add text labels to each column
    for rect in rects1 + rects2:
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width() / 2,
                height,
                int(height),
                ha='center',
                va='bottom',
                fontsize=16,
                )

    # Set tick labels and title
    ax.set_xticks(x)
    ax.set_xticklabels(labels,
                       rotation=45,
                       ha='right',
                       )
    ax.set_title(title)

    # return the figure
    return fig
# -----------------------------------------------------------------------------


# Make a donut Chart with all Machines and plot the total in the middle
# -----------------------------------------------------------------------------
def create_donut_chart(df_donut, machine_names, title):
    """Create a donut chart with the total number of boxes for a given set of machines, based on a pandas DataFrame.

    Args:
        df_donut (pd.DataFrame): A pandas DataFrame containing the data to be plotted.
        machine_names (List[str]): A list of strings representing the names of the machines to be included in the chart.
        title (str): A string with the title of the chart.

    Returns:
        plt.Figure: A matplotlib Figure object containing the resulting donut chart.

    Example:
        >>> df_donut = pd.read_csv('data.csv')
        >>> create_donut_chart(df_donut, ['Machine A', 'Machine B'], 'Total Boxes for Machines A and B')
    """
    # Filter the rows to include only the last available month
    df_donut['DateTime'] = pd.to_datetime(df_donut['DateTime'])
    last_month = df_donut['DateTime'].max()
    df_last_month = df_donut[df_donut['DateTime'] == last_month]

    # Filter the rows to include only the desired machines
    df_machines = df_last_month[df_last_month['Machine'].isin(machine_names)]

    # Calculate the total number of boxes for the selected machines
    total_boxes = df_machines['Boxes'].sum()

    # Create a pie chart with the selected machines
    colors = [c for c in palette_list if c != 'grey']
    fig, ax = plt.subplots()
    wedges, texts, autotexts = ax.pie(df_machines['Boxes'],
                                      labels=df_machines['Machine'],
                                      colors=colors,
                                      autopct='%1.1f%%',
                                      startangle=90,
                                      textprops={'fontsize': 14},
                                      wedgeprops={'linewidth': 7,
                                                  'edgecolor': 'white',
                                                  }
                                      )
    center_circle = plt.Circle((0, 0),
                               0.5,
                               color='white',
                               )
    fig = plt.gcf()
    fig.gca().add_artist(center_circle)
    plt.setp(autotexts,
             size=16,
             weight="bold",
             )
    plt.setp(texts,
             size=16,
             )

    # Add the total number of boxes to the center of the chart
    ax.text(0,
            0,
            total_boxes,
            ha='center',
            va='center',
            fontsize=24,
            )

    # Set the title of the chart
    ax.set_title(title + ' ({})'.format(
        last_month.strftime('%b %Y')),
        fontsize=20,
    )

    # set axis equal to ensure circle is drawn as a circle
    plt.axis('equal')

    return fig
# -----------------------------------------------------------------------------


# create a single line chart that shows the total daily produced boxes
# -----------------------------------------------------------------------------
def create_single_lineplot(df, machine_names, title):
    """
    Creates a line plot of box values for a specific machine for each day
    of the month.

    Args:
    - df (pd.DataFrame): the dataframe containing the data to plot
    - palette_list (list): a list of colors to use for the plot
    - machine_name (str): the name of the machine to plot data for
    - filename (str): the name of the file to save the plot to

    Returns:
    - None
    """
    # format DateTime to dd/mm
    df['DateTime'] = pd.to_datetime(df['DateTime'])
    df['DateTime'] = df['DateTime'].dt.strftime('%d/%m')

    # filter for the specified machine
    machine_df = df[df['Machine'] == machine_names]

    # create the line plot, move the legend to the bottom
    fig, ax = plt.subplots()
    machine_df.plot(x='DateTime', y='Boxes', color=palette_list[4], ax=ax)
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

    # TODO:set
    # save the chart to a file
    return fig
# -----------------------------------------------------------------------------


# create a grouped barplot showing daily produced boxes per machine
# -----------------------------------------------------------------------------
def create_grouped_barplot(df_barplot, machine_names, title):
    """
    Create a grouped barplot with the total number of boxes for a given set of machines.

    Args:
        df_barplot (pd.DataFrame): A pandas DataFrame containing the data to be plotted.
        machine_names (List[str]): A list of strings representing the names of the machines to be included in the chart.
        title (str): A string with the title of the chart.

    Returns:
        plt.Figure: A matplotlib Figure object containing the resulting grouped bar plot.

    Example:
        Create a grouped barplot for machines A and B:

        >>> df_barplot = pd.read_csv('data.csv')
        >>> create_grouped_barplot(df_barplot, ['Machine A', 'Machine B'], 'Total Boxes for Machines A and B')
    """
    # Format DateTime to dd/mm
    df_barplot['DateTime'] = pd.to_datetime(df_barplot['DateTime'])
    df_barplot['DateTime'] = df_barplot['DateTime'].dt.strftime('%d/%m')

    # Create grouped barplot with legend at bottom
    fig, ax = plt.subplots()
    sns.barplot(x='DateTime',
                y='Boxes',
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
    # ax.set(xlabel=None)
    # TODO: set title
    plt.box(False)
    plt.xticks(rotation=45)

    # return the figure
    return fig
# -----------------------------------------------------------------------------


# create a multiline plot that shows each machine in a subplot
# -----------------------------------------------------------------------------
def create_multi_lineplot(df_lineplot, machine_names, title):
    """
    Create a set of line plots showing the box counts over time for each machine.

    Args:
        df (pd.DataFrame): A pandas DataFrame containing the data to be plotted.
        machine_names (List[str]): A list of strings representing the names of the machines to be included in the chart.
        palette_list (List[str]): A list of color codes to be used for each machine.
        title (str): A string with the title of the chart.

    Returns:
        plt.Figure: A matplotlib Figure object containing the resulting line plots.

    Example:
        Create a grouped barplot for machines A and B:

        >>> df_lineplot = pd.read_csv('data.csv')
        >>> create_lineplot(df_barplot, ['Machine A', 'Machine B'], 'Total Boxes for Machines A and B')
    """

    # format DateTime to dd/mm
    df_lineplot['DateTime'] = pd.to_datetime(df_lineplot['DateTime'])
    df_lineplot['DateTime'] = df_lineplot['DateTime'].dt.strftime('%d/%m')

    # Create a list of subplots
    fig, axs = plt.subplots(2, 2, figsize=(10, 8), sharey=True)

    # Flatten the axs array to allow for easier iteration
    axs = axs.flatten()

    # Iterate over each machine name and corresponding color
    for i, (machine, color) in enumerate(zip(machine_names, palette_list)):
        # Create a filtered dataframe for the current machine
        curr_df = df_lineplot[df_lineplot["machine"] == machine]

        # Create a line plot for the current machine
        axs[i].plot(curr_df["DateTime"], curr_df["Boxes"],
                    color="lightgrey", linewidth=1)
        axs[i].plot(curr_df["DateTime"], curr_df["Boxes"],
                    color=color, linewidth=2)

        # Set the title for the current subplot
        axs[i].set_title(machine)

        # Set the x-axis label for the current subplot
        axs[i].set_xlabel("Date")

        # Rotate the x-axis labels for readability
        axs[i].tick_params(axis="x", rotation=45)

    # Set the y-axis label for the entire figure
    fig.text(0.04, 0.5, "Boxes", va="center", rotation="vertical")

    # Set the overall title for the entire figure
    fig.suptitle("Box counts by machine", fontsize=16)

    # Adjust the layout of the subplots to improve readability
    plt.subplots_adjust(wspace=0.05, hspace=0.3)

    return fig
# -----------------------------------------------------------------------------


# create a 2x2 barplot to show stuff by day and machine.
# -----------------------------------------------------------------------------
def create_multi_barplot(df_mbp, machine_names, title):

    # format DateTime to dd/mm
    df_mbp['DateTime'] = pd.to_datetime(df_mbp['DateTime'])
    df_mbp['DateTime'] = df_mbp['DateTime'].dt.strftime('%d/%m')

    fig, axs = plt.subplots(2, 2, figsize=(10, 8), sharey=True)

    # Flatten the axs array to allow for easier iteration
    axs = axs.flatten()

    # Iterate over each machine name and corresponding color
    for i, (machine, color) in enumerate(zip(machine_names, palette_list)):

        # Create a filtered dataframe for the current machine
        curr_df = df_mbp[df_mbp["Machine"] == machine]

        axs[i].bar(curr_df["DateTime"],
                   curr_df["Boxes"],
                   color=color,
                   linewidth=2,
                   )

        # Set the title for the current subplot
        axs[i].set_title(machine)

        # Set the x-axis label for the current subplot
        axs[i].set_xlabel("Date")

        # Rotate the x-axis labels for readability
        axs[i].tick_params(axis="x", rotation=45)

    # Set the y-axis label for the entire figure
    fig.text(0.04, 0.5, "Boxes", va="center", rotation="vertical")

    # Set the overall title for the entire figure
    fig.suptitle("Box counts by machine", fontsize=16)

    # Adjust the layout of the subplots to improve readability
    plt.subplots_adjust(wspace=0.05, hspace=0.3)

    plt.show()
# -----------------------------------------------------------------------------
