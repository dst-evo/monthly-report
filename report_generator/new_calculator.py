import datetime


def calculate_total_seconds_worked():
    """
    Calculates the total amount of seconds worked between the given start and end dates.

    Returns:
    int: The total number of seconds worked in the period.
    """

    # get the current date and calculate the first/last day of the past month
    now = datetime.datetime.now()
    start_date = datetime.datetime(now.year, now.month - 1, 1)
    end_date = datetime.datetime(
        now.year, now.month, 1) - datetime.timedelta(days=1)

    # Define the start and end times for each workday
    weekday_start_time = datetime.time(hour=5, minute=0, second=0)
    weekday_end_time = datetime.time(hour=23, minute=0, second=0)
    saturday_start_time = datetime.time(hour=5, minute=0, second=0)
    saturday_end_time = datetime.time(hour=20, minute=0, second=0)

    # Calculate the total seconds worked
    total_seconds = 0
    current_date = start_date
    while current_date <= end_date:
        if current_date.weekday() < 5:  # Weekdays
            workday_seconds = (datetime.datetime.combine(current_date, weekday_end_time) -
                               datetime.datetime.combine(current_date, weekday_start_time)).total_seconds()
        elif current_date.weekday() == 5:  # Saturday
            workday_seconds = (datetime.datetime.combine(current_date, saturday_end_time) -
                               datetime.datetime.combine(current_date, saturday_start_time)).total_seconds()
        else:  # Sunday
            workday_seconds = 0
        total_seconds += workday_seconds
        current_date += datetime.timedelta(days=1)

    # Return the result
    return total_seconds
