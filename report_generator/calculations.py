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


def get_ws_pm():
    """
    Calculate the total number of working seconds in the previous month based on a standard 18-hour workday from Monday 
    to Friday and 9 or 18-hour workday on Saturdays and Sundays, depending on the month.

    Returns:
    --------
    int:
        The total number of working seconds in the previous month.
    """
    today = dt.date.today()
    first = today.replace(day=1)
    lastMonth = first - dt.timedelta(days=1)
    lastMonth.month
    working_hours = 0
    for i in range(1, 32):
        try:
            thisdate = dt.date(lastMonth.year, lastMonth.month, i)
        except (ValueError):
            break
        if thisdate.weekday() < 5:  # Monday == 0, Sunday == 6
            working_hours += 18
        if (lastMonth.month in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]):
            if thisdate.weekday() == 5:
                working_hours += 9
        elif lastMonth.month == 11:
            if thisdate.weekday() == 5:
                working_hours += 18
        elif lastMonth.month == 12:
            if (thisdate.weekday() in [5, 6]):
                working_hours += 18
    # print(working_hours * 3600)
    return (working_hours*3600)
