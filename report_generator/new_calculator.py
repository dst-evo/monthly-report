import datetime as dt
import matplotlib as mpl
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
    # Check if all the entries contain a ':'
    if not all(':' in str(val) for val in values):
        raise ValueError("All input values must be in 'hh:mm' format")

    total_seconds = sum(
        dt.timedelta(hours=int(h), minutes=int(m)).total_seconds()
        for h, m in (str(x).split(":") for x in values)
    )
    return total_seconds


def percentage_to_float(df, col_name):
    """
    Convert a percentage string to a float value.

    Parameters:
    df (pandas.DataFrame): A DataFrame with a column containing percentage strings.
    col_name (str): Name of the column containing the percentage strings.

    Returns:
    pandas.DataFrame: The input DataFrame with the specified column converted to floats.
    """
    if col_name not in df.columns:
        raise ValueError(f"Input DataFrame must have a '{col_name}' column")

    df[col_name] = df[col_name].apply(
        lambda x: x.replace("%", "") if isinstance(
            x, str) and x.endswith('%') else x
    ).astype(float) / 100

    return df


def calculate_total_seconds_worked(start_date, end_date):
    """
    Calculates the total amount of seconds worked between the given start and end dates.

    Returns:
    int: The total number of seconds worked in the period.
    """

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


def time_to_minutes(time_str):
    """Converts time in format 'hh:mm' to total minutes."""
    hours, minutes = map(int, time_str.split(':'))
    return hours*60 + minutes


def convert_seconds_to_hhmm(seconds):
    # Convert seconds to "hh:mm" format
    return f"{int(seconds // 3600)}:{int((seconds % 3600) // 60)}"


def to_percent(y, position):
    # Ignore the passed in position. This has the effect of scaling the default
    # tick locations.
    s = str(100 * y)

    # The percent symbol needs escaping in latex
    if mpl.rcParams['text.usetex'] is True:
        return s + r'$\%$'
    else:
        return s + '%'


def format_percentage(n):
    """Format a float as a percentage string with a maximum of three significant figures."""
    # Increase the precision for the comparison
    n *= 1000
    # Decide the number of decimal places based on the value
    if n >= 100:    # n >= 0.1
        format_str = "{:.0f}%"
    elif n >= 10:  # n >= 0.01
        format_str = "{:.1f}%"
    else:                    # smaller numbers
        format_str = "{:.2f}%"
    # Return the formatted string
    return format_str.format(n / 10)
