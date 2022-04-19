# import libraries
import pandas as pd
import datetime as dt
import os
import subprocess


# import scripts
import calculations as calc
import img_generator as ig

tags = ['L1 - VPM B (4958)', 'L2 - VPM A (4959)',
        'L3 - VPM C (4960)', 'L4 - VPM D (4961)']
os.system('CLS')
print('gathering historical data')
# !!YOU HAVE TO ADJUST THIS BY HAND UNTIL API IS AVAILABLE!!
# Historic Values to compare month over month
# ----------------------------------------------------------- #
hv_total = [499634, 390405, 430625]
hv_bph_avg_b = [463, 471, 511]
hv_bph_avg_a = [564, 508, 508]
hv_bph_avg_c = [473, 440, 490]
hv_bph_avg_d = [490, 447, 522]
hv_bph_avg_cmc_b = [598, 616, 621]
hv_bph_avg_cmc_a = [744, 731, 713]
hv_bph_avg_cmc_c = [670, 664, 632]
hv_bph_avg_cmc_d = [663, 681, 685]
hv_bbm_b = [0.0544, 0.0387, 0.0455]
hv_bbm_a = [0.0282, 0.0276, 0.0342]
hv_bbm_c = [0.034, 0.0395, 0.0355]
hv_bbm_d = [0.0261, 0.027, 0.0218]
hv_avg_avail_b = [0.873, 0.911, 0.863]
hv_avg_avail_a = [0.915, 0.925, 0.904]
hv_avg_avail_c = [0.886, 0.898, 0.878]
hv_avg_avail_d = [0.92, 0.918, 0.913]
# ----------------------------------------------------------- #
# create date range for the months since start of year
dates = pd.date_range(start="2022-01-01", end=dt.date.today().replace(day=1) - dt.timedelta(days=1),
                      freq='MS')
os.system('CLS')
print('creating historical dataframe')
# create dataframe with all historic values, date as index
historic = {
    'total': hv_total,
    'bph_avg_b': hv_bph_avg_b,
    'bph_avg_a': hv_bph_avg_a,
    'bph_avg_c': hv_bph_avg_c,
    'bph_avg_d': hv_bph_avg_d,
    'bph_avg_cmc_b': hv_bph_avg_cmc_b,
    'bph_avg_cmc_a': hv_bph_avg_cmc_a,
    'bph_avg_cmc_c': hv_bph_avg_cmc_c,
    'bph_avg_cmc_d': hv_bph_avg_cmc_d,
    'bbm_b': hv_bbm_b,
    'bbm_a': hv_bbm_a,
    'bbm_c': hv_bbm_c,
    'bbm_d': hv_bbm_d,
    'avg_avail_b': hv_avg_avail_b,
    'avg_avail_a': hv_avg_avail_a,
    'avg_avail_c': hv_avg_avail_c,
    'avg_avail_d': hv_avg_avail_d
}
df_historic = pd.DataFrame(historic, index=dates)

os.system('CLS')
print('converting csv-files to dataframes')
# create dataframes from .csv-files for each machine
df_a = pd.read_csv(r'./aggregate_data/aggregate_data_a.csv',
                   sep=';', parse_dates=['date'], index_col=['date'])
df_b = pd.read_csv(r'./aggregate_data/aggregate_data_b.csv',
                   sep=';', parse_dates=['date'], index_col=['date'])
df_c = pd.read_csv(r'./aggregate_data/aggregate_data_c.csv',
                   sep=';', parse_dates=['date'], index_col=['date'])
df_d = pd.read_csv(r'./aggregate_data/aggregate_data_d.csv',
                   sep=';', parse_dates=['date'], index_col=['date'])

df_total = calc.calculate_totals(df_a, df_b, df_c, df_d)

os.system('CLS')
# Create Plots for various datapoints
# ----------------------------------------------------------- #
# total produced boxes per day
print('Printernoises brrrrrrrrrrrrrrrrr\n|█---------------|')
ig.single_linechart(df_b['produced_boxes'], df_a['produced_boxes'],
                    df_c['produced_boxes'], df_d['produced_boxes'], df_a.index, 'pb_tot')
#
# produced per day and machine
os.system('CLS')
print('Printernoises brrrrrrrrrrrrrrrrr\n|██--------------|')
ig.daily_barplot(df_b['produced_boxes'], df_a['produced_boxes'],
                 df_c['produced_boxes'], df_d['produced_boxes'], df_a.index, 'pb')

# Donut chart of total Produced Boxes per machine
os.system('CLS')
print('Printernoises brrrrrrrrrrrrrrrrr\n|███-------------|')
ig.donut_chart(df_total[9:13], 'total_box_pm')

# total produced boxes month over month
os.system('CLS')
print('Printernoises brrrrrrrrrrrrrrrrr\n|████------------|')
ig.historic_single_barplot(df_historic['total'], 'total')


# throughput per day and machine
os.system('CLS')
print('Printernoises brrrrrrrrrrrrrrrrr\n|█████-----------|')
ig.multi_line(df_b['machine_tp'], df_a['machine_tp'],
              df_c['machine_tp'], df_d['machine_tp'], df_a.index, 'm_tp')

# average bph per machine month over month
os.system('CLS')
print('Printernoises brrrrrrrrrrrrrrrrr\n|██████----------|')
ig.hisoric_multi(
    df_historic[['bph_avg_b', 'bph_avg_a', 'bph_avg_c', 'bph_avg_d']], 'm_tp_avg')

# throughput per day and machine according to CMC
os.system('CLS')
print('Printernoises brrrrrrrrrrrrrrrrr\n|███████---------|')
ig.multi_line(df_b['machine_tp_cmc'], df_a['machine_tp_cmc'],
              df_c['machine_tp_cmc'], df_d['machine_tp_cmc'], df_a.index, 'm_tp_cmc')

# average bph per machine month over month according to CMC
os.system('CLS')
print('Printernoises brrrrrrrrrrrrrrrrr\n|████████--------|')
ig.hisoric_multi(
    df_historic[['bph_avg_cmc_b', 'bph_avg_cmc_a', 'bph_avg_cmc_c', 'bph_avg_cmc_d']], 'm_tp_cmc_avg')

# Total time divided into different states of the maschine
os.system('CLS')
print('Printernoises brrrrrrrrrrrrrrrrr\n|█████████-------|')
ig.pie_chart(
    df_d[['run_time', 'idle_time', 'error_time', 'corr_maint_time', 'prev_maint_time']], 'Total')

# relative time in each machine state (or machine turned off/unknown state)
os.system('CLS')
print('Printernoises brrrrrrrrrrrrrrrrr\n|██████████------|')
ig.pie_chart(
    df_b[['run_time', 'idle_time', 'error_time', 'corr_maint_time', 'prev_maint_time']], tags[0])
ig.pie_chart(
    df_a[['run_time', 'idle_time', 'error_time', 'corr_maint_time', 'prev_maint_time']], tags[1])
ig.pie_chart(
    df_c[['run_time', 'idle_time', 'error_time', 'corr_maint_time', 'prev_maint_time']], tags[2])
ig.pie_chart(
    df_d[['run_time', 'idle_time', 'error_time', 'corr_maint_time', 'prev_maint_time']], tags[3])

# absolute total bad boxes per day
os.system('CLS')
print('Printernoises brrrrrrrrrrrrrrrrr\n|███████████-----|')
ig.single_linechart(df_b['abs_bad_boxes'], df_a['abs_bad_boxes'],
                    df_c['abs_bad_boxes'], df_d['abs_bad_boxes'], df_a.index, 'abs_bb_tot')

# absolute bad boxes per day and machine
os.system('CLS')
print('Printernoises brrrrrrrrrrrrrrrrr\n|████████████----|')
ig.daily_barplot(df_b['abs_bad_boxes'], df_a['abs_bad_boxes'],
                 df_c['abs_bad_boxes'], df_d['abs_bad_boxes'], df_a.index, 'abs_bb_pm', isbb=True)

# relative bad boxes per day and machine
os.system('CLS')
print('Printernoises brrrrrrrrrrrrrrrrr\n|█████████████---|')
ig.daily_barplot(df_b['rel_bad_boxes'], df_a['rel_bad_boxes'],
                 df_c['rel_bad_boxes'], df_d['rel_bad_boxes'], df_a.index, 'rel_bb_pm', True, False)

# relative bad boxes average month over month
os.system('CLS')
print('Printernoises brrrrrrrrrrrrrrrrr\n|██████████████--|')
ig.hisoric_multi_percent(
    df_historic[['bbm_b', 'bbm_a', 'bbm_c', 'bbm_d']], 'bbm', False)

# daily availability per day and machine
os.system('CLS')
print('Printernoises brrrrrrrrrrrrrrrrr\n|███████████████-|')
ig.daily_barplot(df_b['op_avail'], df_a['op_avail'],
                 df_c['op_avail'], df_d['op_avail'], df_a.index, 'op_avail', True, True)

# average availability per machine month over month
os.system('CLS')
print('Printernoises brrrrrrrrrrrrrrrrr\n|████████████████|')
ig.hisoric_multi_percent(
    df_historic[['avg_avail_b', 'avg_avail_a', 'avg_avail_c', 'avg_avail_d']], 'avg_avail', True)

# ----------------------------------------------------------- #


os.system('CLS')
# changing working directory to output subfolder
os.chdir(os.getcwd() + '/output')
# call lualatex and compile the texfile
subprocess.check_call(['lualatex', 'monthly_report.tex'])

os.system('CLS')
print('~~ FIN ~~')
