import os
import pandas as pd
import new_calculator as nc


def merge_time_data(delimiter=';', columns=['DateTime', 'Machine', 'Hours']):
    """
    Merge time data from multiple CSV files and return a dataframe with renamed columns.

    Parameters:
    delimiter (str, optional): The delimiter used in the CSV files. Default is ';'.
    columns (list, optional): The column names to be read from the CSV files. Default is ['DateTime', 'Machine', 'Hours'].

    Returns:
    pandas.DataFrame: A dataframe containing the merged data from all CSV files, with renamed columns based on the source file and missing values replaced with 0.
    """

    file_paths = {
        "corr_maint": "./raw_data/corr_maint_time.csv",
        "error": "./raw_data/error_time.csv",
        "idle": "./raw_data/idle_time.csv",
        "prev_maint": "./raw_data/prev_maint_time.csv",
        "run_time": "./raw_data/run_time.csv",
    }

    dataframes = {}

    for key, path in file_paths.items():
        if os.path.isfile(path):
            try:
                dataframes[key] = pd.read_csv(
                    path, delimiter=delimiter, usecols=columns)
            except Exception as e:
                print(f"Error occurred while reading file {path}: {e}")
        else:
            print(f"File {path} does not exist.")

    # Merge all the dataframes on 'Machine' and 'DateTime'
    df_time_merged = pd.merge(dataframes['corr_maint'], dataframes['error'], on=[
                              "Machine", "DateTime"], how="outer", suffixes=('_corr_maint', '_error'))
    df_time_merged = pd.merge(df_time_merged, dataframes['idle'], on=[
                              "Machine", "DateTime"], how="outer")
    df_time_merged = pd.merge(df_time_merged, dataframes['prev_maint'], on=[
                              "Machine", "DateTime"], how="outer")
    df_time_merged = pd.merge(df_time_merged, dataframes['run_time'], on=[
                              "Machine", "DateTime"], how="outer")

    # Rename the columns
    df_time_merged = df_time_merged.rename(columns={'Hours': 'Hours_run_time'})
    df_time_merged = df_time_merged.rename(
        columns={'Hours_x': 'Hours_idle_time'})
    df_time_merged = df_time_merged.rename(
        columns={'Hours_y': 'Hours_prev_maint'})

    # Replace missing values with 0
    df_time_merged.fillna(0, inplace=True)

    return df_time_merged


def merge_historical_data(delimiter=';'):
    """
    Merge historical data from multiple CSV files and return a dataframe with renamed columns.

    Parameters:
    delimiter (str, optional): The delimiter used in the CSV files. Default is ','.

    Returns:
    pandas.DataFrame: A dataframe containing the merged data from all CSV files, with renamed columns based on the source file and missing values replaced with 0.
    """

    file_paths = {
        "boxes": "./raw_data/historic_boxes.csv",
        "machine_tp": "./raw_data/historic_machine_tp.csv",
        "machine_tp_cmc": "./raw_data/historic_machine_tp_cmc.csv",
        "bad_boxes": "./raw_data/historic_bad_boxes.csv",
        "op_avail": "./raw_data/historic_op_avail.csv",
        "carton_ch1": "./raw_data/carton_ch1.csv",
        "carton_ch2": "./raw_data/carton_ch2.csv",
    }

    columns = {
        "boxes": ['DateTime', 'Machine', 'Boxes'],
        "machine_tp": ['DateTime', 'Machine', 'Boxes/hour'],
        "machine_tp_cmc": ['DateTime', 'Machine', 'Boxes/hour'],
        "bad_boxes": ['DateTime', 'Machine', 'Boxes%', 'Quantity'],
        "op_avail": ['DateTime', 'Machine', 'Time%'],
        "carton_ch1": ['DateTime', 'Machine', 'mt'],
        "carton_ch2": ['DateTime', 'Machine', 'mt'],
    }

    dataframes = {}

    for key, path in file_paths.items():
        if os.path.isfile(path):
            try:
                dataframes[key] = pd.read_csv(
                    path, delimiter=delimiter, usecols=columns[key])
            except Exception as e:
                print(f"Error occurred while reading file {path}: {e}")
        else:
            print(f"File {path} does not exist.")

    # Merge all the dataframes on 'Machine' and 'DateTime'
    df_merged = pd.merge(dataframes['boxes'], dataframes['machine_tp'], on=[
                         "Machine", "DateTime"], how="outer", suffixes=('_boxes', '_machine_tp'))
    df_merged = pd.merge(df_merged, dataframes['machine_tp_cmc'], on=[
                         "Machine", "DateTime"], how="outer")
    df_merged = pd.merge(df_merged, dataframes['bad_boxes'], on=[
                         "Machine", "DateTime"], how="outer")
    df_merged = pd.merge(df_merged, dataframes['op_avail'], on=[
                         "Machine", "DateTime"], how="outer")
    df_merged = pd.merge(df_merged, dataframes['carton_ch1'], on=[
                         "Machine", "DateTime"], how="outer")
    df_merged = pd.merge(df_merged, dataframes['carton_ch2'], on=[
                         "Machine", "DateTime"], how="outer")

    # Rename the columns
    df_merged = df_merged.rename(columns={'Boxes/hour_x': 'machine_tp',
                                          'Boxes/hour_y': 'machine_tp_cmc',
                                          'Boxes%': 'rel_bad_boxes',
                                          'Quantity': 'abs_bad_boxes',
                                          'Time%': 'op_avail',
                                          'mt_x': 'carton_ch1',
                                          'mt_y': 'carton_ch2',
                                          })

    # Replace missing values with 0
    df_merged.fillna(0, inplace=True)

    # calculate squaremeters per box
    df_merged = nc.calculate_carton_per_box(df_merged)

    return df_merged


def merge_monthly_data(delimiter=';'):
    """
    Merge historical data from multiple CSV files and return a dataframe with renamed columns.

    Parameters:
    delimiter (str, optional): The delimiter used in the CSV files. Default is ','.

    Returns:
    pandas.DataFrame: A dataframe containing the merged data from all CSV files, with renamed columns based on the source file and missing values replaced with 0.
    """

    file_paths = {
        "boxes": "./raw_data/daily_boxes.csv",
        "machine_tp": "./raw_data/machine_tp.csv",
        "machine_tp_cmc": "./raw_data/machine_tp_cmc.csv",
        "bad_boxes": "./raw_data/bad_boxes.csv",
        "op_avail": "./raw_data/op_avail.csv"
    }

    columns = {
        "boxes": ['DateTime', 'Machine', 'Boxes'],
        "machine_tp": ['DateTime', 'Machine', 'Boxes/hour'],
        "machine_tp_cmc": ['DateTime', 'Machine', 'Boxes/hour'],
        "bad_boxes": ['DateTime', 'Machine', 'Boxes%', 'Quantity'],
        "op_avail": ['DateTime', 'Machine', 'Time%']
    }

    dataframes = {}

    for key, path in file_paths.items():
        if os.path.isfile(path):
            try:
                dataframes[key] = pd.read_csv(
                    path, delimiter=delimiter, usecols=columns[key])
            except Exception as e:
                print(f"Error occurred while reading file {path}: {e}")
        else:
            print(f"File {path} does not exist.")

    # Merge all the dataframes on 'Machine' and 'DateTime'
    df_merged = pd.merge(dataframes['boxes'], dataframes['machine_tp'], on=[
                         "Machine", "DateTime"], how="outer", suffixes=('_boxes', '_machine_tp'))
    df_merged = pd.merge(df_merged, dataframes['machine_tp_cmc'], on=[
                         "Machine", "DateTime"], how="outer")
    df_merged = pd.merge(df_merged, dataframes['bad_boxes'], on=[
                         "Machine", "DateTime"], how="outer")
    df_merged = pd.merge(df_merged, dataframes['op_avail'], on=[
                         "Machine", "DateTime"], how="outer")

    # Rename the columns
    df_merged = df_merged.rename(columns={'Boxes/hour_x': 'machine_tp', 'Boxes/hour_y': 'machine_tp_cmc',
                                 'Boxes%': 'rel_bad_boxes', 'Quantity': 'abs_bad_boxes', 'Time%': 'op_avail'})

    # Replace missing values with 0
    df_merged.fillna(0, inplace=True)

    return df_merged


def read_csv_to_df(file_path):
    """
    Read a CSV file and convert it into a pandas DataFrame.

    Parameters:
    file_path (str): The path to the CSV file.

    Returns:
    pandas.DataFrame: A DataFrame populated with the CSV data.
    """
    if not isinstance(file_path, str) or not file_path.endswith('.csv'):
        raise ValueError("file_path must be a string ending with '.csv'")
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"No file found at provided path: {file_path}")

    df = pd.read_csv(file_path)

    return df
