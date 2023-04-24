import datetime as dt

# TODO: standardize docstrings, add examples to docstrings


def round_up(number, decimal_places=0):
    """
    Round a number up to the nearest multiple of 10^(-decimals).

    Parameters:
    number (float): The number to round up.
    decimals_places (int, optional): The number of decimal places to round up to. Default is 0.

    Returns:
    float: The rounded-up value.
    """
    if not isinstance(number, (int, float)):
        raise ValueError("number must be a numeric value")
    if not isinstance(decimal_places, int):
        raise ValueError("decimal_places must be an integer")

    multiplier = 10 ** decimal_places
    return round(number * multiplier, ndigits=None, up=True) / multiplier


def convert_to_seconds(values):
    """
    Convert a series of hh:mm elements to seconds and sum them.

    Parameters:
    values (list or pandas.Series): The values to convert to seconds.

    Returns:
    int: The total number of seconds.
    """
    if not all(":") in values:
        raise ValueError("All input values must be in 'hh:mm' format")

    total_seconds = sum(
        dt.timedelta(hours=int(h), minutes=int(m)).total_seconds()
        for h, m in (x.split(":") for x in values)
    )
    return total_seconds


def percentage_to_float(values):
    """
    Convert a percentage string to a float value.

    Parameters:
    values (pandas.DataFrame): A DataFrame with a 'rel_bad_boxes' column containing percentage strings.

    Returns:
    pandas.DataFrame: The input DataFrame with the 'rel_bad_boxes' column converted to floats.
    """
    if not all(col in values.columns for col in ["rel_bad_boxes"]):
        raise ValueError("Input DataFrame must have a 'rel_bad_boxes' column")

    values["rel_bad_boxes"] = values["rel_bad_boxes"].apply(
        lambda x: x.replace("%", "")).astype(float) / 100
    return values


def calculate_total_seconds_worked():
    """
    Calculates the total amount of seconds worked between the given start and end dates.

    Returns:
    int: The total number of seconds worked in the period.
    """

    # get the current date and calculate the first/last day of the past month
    now = dt.datetime.now()
    start_date = dt.datetime(now.year, now.month - 1, 1)
    end_date = dt.datetime(
        now.year, now.month, 1) - dt.timedelta(days=1)

    # Define the start and end times for each workday
    weekday_start_time = dt.time(hour=5, minute=0, second=0)
    weekday_end_time = dt.time(hour=23, minute=0, second=0)
    saturday_start_time = dt.time(hour=5, minute=0, second=0)
    saturday_end_time = dt.time(hour=20, minute=0, second=0)

    # Calculate the total seconds worked
    total_seconds = 0
    current_date = start_date
    while current_date <= end_date:
        if current_date.weekday() < 5:  # Weekdays
            workday_seconds = (dt.datetime.combine(current_date, weekday_end_time) -
                               dt.datetime.combine(current_date, weekday_start_time)).total_seconds()
        elif current_date.weekday() == 5:  # Saturday
            workday_seconds = (dt.datetime.combine(current_date, saturday_end_time) -
                               dt.datetime.combine(current_date, saturday_start_time)).total_seconds()
        else:  # Sunday
            workday_seconds = 0
        total_seconds += workday_seconds
        current_date += dt.timedelta(days=1)

    # Return the result
    return total_seconds
