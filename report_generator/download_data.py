# download data from dashboard to .csv files

import get_data_from_dashboard as gdfd


def download_data_parts(driver, start_date_str, end_date_str, second_start_date_str):
    """
    Download multiple data parts from the dashboard using the given parameters.

    Parameters:
    driver (webdriver): The Selenium WebDriver instance to interact with the page.
    start_date_str (str): The start date for the data range in the format "dd/mm/yyyy hh:mm".
    end_date_str (str): The end date for the data range in the format "dd/mm/yyyy hh:mm".
    second_start_date_str (str): The second start date for the data range in the format "dd/mm/yyyy hh:mm".

    Returns:
    None
    """
    print("Downloading Data part 1")
    gdfd.configure_and_download_data(driver,
                                     "month",
                                     "yes",
                                     second_start_date_str,
                                     end_date_str,
                                     "Produced boxes",
                                     "boxes_total_current_interval.csv",
                                     )

    print("Downloading Data part 2")
    gdfd.configure_and_download_data(driver,
                                     "day",
                                     "no",
                                     start_date_str,
                                     end_date_str,
                                     "Produced boxes",
                                     "produced_boxes_daily.csv",
                                     )

    print("Downloading Data part 3")
    gdfd.configure_and_download_data(driver,
                                     "day",
                                     "no",
                                     start_date_str,
                                     end_date_str,
                                     "Throughput",
                                     "machine_tp.csv"
                                     )

    print("Downloading Data part 4")
    gdfd.configure_and_download_data(driver,
                                     "day",
                                     "no",
                                     start_date_str,
                                     end_date_str,
                                     "Throughput CMC",
                                     "machine_tp_cmc.csv"
                                     )

    print("Downloading Data part 5")
    gdfd.configure_and_download_data(driver,
                                     "day",
                                     "no",
                                     start_date_str,
                                     end_date_str,
                                     "Idle time",
                                     "idle_time.csv"
                                     )

    print("Downloading Data part 6")
    gdfd.configure_and_download_data(driver,
                                     "day",
                                     "no",
                                     start_date_str,
                                     end_date_str,
                                     "Run time",
                                     "run_time.csv"
                                     )

    print("Downloading Data part 7")
    gdfd.configure_and_download_data(driver,
                                     "day",
                                     "no",
                                     start_date_str,
                                     end_date_str,
                                     "Error time",
                                     "error_time.csv"
                                     )

    print("Downloading Data part 8")
    gdfd.configure_and_download_data(driver,
                                     "day",
                                     "no",
                                     start_date_str,
                                     end_date_str,
                                     "Corrective maintenance time",
                                     "corr_maint_time.csv"
                                     )

    print("Downloading Data part 9")
    gdfd.configure_and_download_data(driver,
                                     "day",
                                     "no",
                                     start_date_str,
                                     end_date_str,
                                     "Preventive maintenance time",
                                     "prev_maint_time.csv"
                                     )

    print("Downloading Data part 9")
    gdfd.configure_and_download_data(driver,
                                     "day",
                                     "no",
                                     start_date_str,
                                     end_date_str,
                                     "Bad boxes: All reasons",
                                     "bad_boxes.csv"
                                     )

    print("Downloading Data part 10")
    gdfd.configure_and_download_data(driver,
                                     "month",
                                     "no",
                                     second_start_date_str,
                                     end_date_str,
                                     "Bad boxes: All reasons",
                                     "bad_boxes_hist.csv"
                                     )

    print("Downloading Data part 11")
    gdfd.configure_and_download_data(driver,
                                     "month",
                                     "no",
                                     second_start_date_str,
                                     end_date_str,
                                     "Throughput",
                                     "machine_tp_hist.csv"
                                     )

    print("Downloading Data part 12")
    gdfd.configure_and_download_data(driver,
                                     "month",
                                     "no",
                                     second_start_date_str,
                                     end_date_str,
                                     "Throughput CMC",
                                     "machine_tp_cmc_hist.csv"
                                     )

    print("Downloading Data part 13")
    gdfd.configure_and_download_data(driver,
                                     "month",
                                     "no",
                                     second_start_date_str,
                                     end_date_str,
                                     "Operational availability",
                                     "op_avail_hist.csv"
                                     )
