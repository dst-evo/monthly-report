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
# TODO: change list to tuple and read from json instead of hardcoded
# ----------------------------------------------------------- #
hv_total = (499634, 390405, 430625, 386275,
            413301, 409882, 388122, 460498, 451645, 445403, 586158,)
hv_bph_avg_b = [463, 471, 511, 470, 494, 419, 373, 461, 456, 465, 441]
hv_bph_avg_a = [564, 508, 508, 504, 501, 477, 523, 512, 525, 493, 566]
hv_bph_avg_c = [473, 440, 490, 485, 491, 417, 428, 447, 451, 511, 472]
hv_bph_avg_d = [490, 447, 522, 541, 502, 457, 472, 449, 471, 525, 473]
hv_bph_avg_cmc_b = [598, 616, 621, 604, 608, 548, 499, 587, 611, 668, 569]
hv_bph_avg_cmc_a = [744, 731, 713, 709, 682, 641, 706, 669, 741, 756, 720]
hv_bph_avg_cmc_c = [670, 664, 632, 634, 636, 570, 678, 607, 624, 692, 632]
hv_bph_avg_cmc_d = [663, 681, 685, 706, 651, 622, 663, 615, 637, 677, 642]
hv_bbm_b = [0.0544, 0.0387, 0.0455, 0.0488,
            0.0477, 0.055, 0.0510, 0.047, 0.0418, 0.0384, 0.0437]
hv_bbm_a = [0.0282, 0.0276, 0.0342, 0.0327,
            0.0346, 0.0407, 0.0277, 0.0225, 0.0208, 0.0229, 0.0264]
hv_bbm_c = [0.034, 0.0395, 0.0355, 0.0354,
            0.0341, 0.0346, 0.0208, 0.0226, 0.0254, 0.0205, 0.0326]
hv_bbm_d = [0.0261, 0.027, 0.0218, 0.0203,
            0.0265, 0.0255, 0.0224, 0.0314, 0.0202, 0.0224, 0.0285]
hv_avg_avail_b = [0.873, 0.911, 0.863, 0.865,
                  0.877, 0.849, 0.8610, 0.881, 0.898, 0.908, 0.866]
hv_avg_avail_a = [0.915, 0.925, 0.904,
                  0.883, 0.879, 0.867, 0.9110, 0.92, 0.923, 0.922, 0.908]
hv_avg_avail_c = [0.886, 0.898, 0.878, 0.878,
                  0.893, 0.888, 0.9150, 0.898, 0.874, 0.906, 0.873]
hv_avg_avail_d = [0.92, 0.918, 0.913, 0.934,
                  0.907, 0.905, 0.9270, 0.889, 0.929, 0.916, 0.905]
# ----------------------------------------------------------- #
# create date range for the months since start of year
dates = pd.date_range(start="2022-05-01", end=dt.date.today().replace(day=1) - dt.timedelta(days=1),
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
print(df_total)
# Total time divided into different states of the maschine
# os.system('CLS')
print('Printernoises brrrrrrrrrrrrrrrrr\n|█████████-------|')
ig.pie_chart(
    # df_total[['run_time', 'idle_time', 'error_time', 'corr_maint_time', 'prev_maint_time']], 'Total')
    df_total[1:6], 'Total')

# relative time in each machine state (or machine turned off/unknown state)
# os.system('CLS')
print('Printernoises brrrrrrrrrrrrrrrrr\n|██████████------|')
ig.pie_chart(
    df_b[['run_time', 'idle_time', 'error_time', 'corr_maint_time', 'prev_maint_time']], tags[0])
ig.pie_chart(
    df_a[['run_time', 'idle_time', 'error_time', 'corr_maint_time', 'prev_maint_time']], tags[1])
ig.pie_chart(
    df_c[['run_time', 'idle_time', 'error_time', 'corr_maint_time', 'prev_maint_time']], tags[2])
ig.pie_chart(
    df_d[['run_time', 'idle_time', 'error_time', 'corr_maint_time', 'prev_maint_time']], tags[3])
breakpoint()

# absolute total bad boxes per day
# os.system('CLS')
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
