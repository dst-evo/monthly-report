import pandas as pd


def merge_time_data(delimiter=';', columns=['DateTime', 'Machine', 'Hours']):
    # Read in all the CSV files
    cm_time = pd.read_csv("./raw_data/corr_maint_time.csv",
                          delimiter=delimiter, usecols=columns)
    et_time = pd.read_csv("./raw_data/error_time.csv",
                          delimiter=delimiter, usecols=columns)
    it_time = pd.read_csv("./raw_data/idle_time.csv",
                          delimiter=delimiter, usecols=columns)
    pm_time = pd.read_csv("./raw_data/prev_maint_time.csv",
                          delimiter=delimiter, usecols=columns)
    rt_time = pd.read_csv("./raw_data/run_time.csv",
                          delimiter=delimiter, usecols=columns)

    # Merge all the dataframes on 'Machine' and 'DateTime'
    df_time_merged = pd.merge(cm_time, et_time, on=[
                              "Machine", "DateTime"], how="outer", suffixes=('_corr_maint', '_error'))
    df_time_merged = pd.merge(df_time_merged, it_time, on=[
                              "Machine", "DateTime"], how="outer")
    df_time_merged = pd.merge(df_time_merged, pm_time, on=[
                              "Machine", "DateTime"], how="outer")
    df_time_merged = pd.merge(df_time_merged, rt_time, on=[
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
