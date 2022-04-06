import math
import datetime


def round_up(n, decimals=0):
    multiplier = 10 ** decimals
    return math.ceil(n*multiplier)/multiplier


def convert_to_seconds(values):
    """ convert a series of hh:mm elements to seconds and add them up """
    total = 0
    for x in values:
        h, m = x.split(':')
        total += int(h) * 3600 + int(m) * 60
    return total


def get_ws_pm():
    """get total working seconds of the past month """
    today = datetime.date.today()
    first = today.replace(day=1)
    lastMonth = first - datetime.timedelta(days=1)
    working_hours = 0
    for i in range(1, 32):
        try:
            thisdate = datetime.date(lastMonth.year, lastMonth.month, i)
        except(ValueError):
            break
        if thisdate.weekday() < 5:  # Monday == 0, Sunday == 6
            working_hours += 18
        if thisdate.weekday() == 5:
            working_hours += 9

    return(working_hours*3600)

# TODO: write function to calculate total:
#           Produced Packages
#           Time in each machine state
#           Absolute bad boxes
#           relative bad boxes
#


def calculate_totals(df_a, df_b, df_c, df_d):
    return 'lolno'
