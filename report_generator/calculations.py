import math
import datetime
import pandas as pd

from numpy import average


def round_up(n, decimals=0):
    multiplier = 10 ** decimals
    return math.ceil(n*multiplier)/multiplier


def convert_to_seconds(values):
    """ convert a series of hh:mm elements to seconds and add them up """
    total = 0
    for x in values:
        h, m = x.split(':')
        total += int(h) * 3600 + int(m) * 60

    print(total)
    return total


def percentage_to_float(values):
    values['rel_bad_boxes'] = values['rel_bad_boxes'].str.rstrip(
        '%').astype('float') / 100
    return values


def get_ws_pm():
    """get total working seconds of the past month """
    today = datetime.date.today()
    first = today.replace(day=1)
    lastMonth = first - datetime.timedelta(days=1)
    lastMonth.month
    working_hours = 0
    for i in range(1, 32):
        try:
            thisdate = datetime.date(lastMonth.year, lastMonth.month, i)
        except(ValueError):
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
    #print(working_hours * 3600)
    return(working_hours*3600)


def calculate_totals(df_a, df_b, df_c, df_d):
    df_total = pd.concat([df_a, df_b, df_c, df_d])
    df_return = []
    percentage_to_float(df_total)
    # calculate total boxes
    df_return.append(sum(df_total['produced_boxes']))
    df_return.append(convert_to_seconds(df_total['run_time']))
    df_return.append(convert_to_seconds(df_total['idle_time']))
    df_return.append(convert_to_seconds(df_total['error_time']))
    df_return.append(convert_to_seconds(df_total['corr_maint_time']))
    df_return.append(convert_to_seconds(df_total['prev_maint_time']))
    df_return.append(get_ws_pm() * 4 - sum(df_return[1:5]))
    df_return.append(sum(df_total['abs_bad_boxes']))
    df_return.append(df_total.where(df_total['run_time'] > '01:00')[
                     'rel_bad_boxes'].mean())
    df_return.append(sum(df_b['produced_boxes']))
    df_return.append(sum(df_a['produced_boxes']))
    df_return.append(sum(df_c['produced_boxes']))
    df_return.append(sum(df_d['produced_boxes']))
    return df_return

    #pd.DataFrame({'Name': [], 'Value': []})
