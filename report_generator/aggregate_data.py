import pandas as pd

# create empty dataframe to be filled with data
df = pd.DataFrame()

# Read date
df['date'] = pd.read_csv("./raw_data/Produced boxes.csv",
                         usecols=['DateTime'], sep=';')

# Read machine ID
df['machine_id'] = pd.read_csv("./raw_data/Produced boxes.csv",
                               usecols=['Machine'], sep=';')

# Read produced boxes
df['produced_boxes'] = pd.read_csv("./raw_data/Produced boxes.csv",
                                   usecols=['Boxes'], sep=';')

# Read relative and absolute bad boxes
df['rel_bad_boxes'] = pd.read_csv(
    "./raw_data/Bad boxes.csv", usecols=['Boxes%'], sep=';')
df['abs_bad_boxes'] = pd.read_csv(
    "./raw_data/Bad boxes.csv", usecols=['Quantity'], sep=';')

# Read run time
df['run_time'] = pd.read_csv(
    "./raw_data/Run Time.csv", usecols=['Hours'], sep=';')

# Read idle time
df['idle_time'] = pd.read_csv(
    "./raw_data/Idle Time.csv", usecols=['Hours'], sep=';')

# Read error time
df['error_time'] = pd.read_csv(
    "./raw_data/Error Time.csv", usecols=['Hours'], sep=';')

# Read corrective maintenance time
df['corr_maint_time'] = pd.read_csv(
    "./raw_data/Corrective Maintenance Time.csv", usecols=['Hours'], sep=';')

# Read preventive maintenance time
df['prev_maint_time'] = pd.read_csv(
    "./raw_data/Preventive Maintenance Time.csv", usecols=['Hours'], sep=';')

# Read operational machine availability
df['op_avail'] = pd.read_csv(
    "./raw_data/Machine availability.csv", usecols=['Time%'], sep=';')
# Read technical machine availability
df['tech_avail'] = pd.read_csv(
    "./raw_data/Machine availability tech.csv", usecols=['Time%'], sep=';')
# Read machine throughput
df['machine_tp'] = pd.read_csv(
    "./raw_data/Machine throughput.csv", usecols=['Boxes/hour'], sep=';')

# Read theoretical machine throughput
df['machine_tp_cmc'] = pd.read_csv(
    "./raw_data/Machine throughput CMC.csv", usecols=['Boxes/hour'], sep=';')

# Read machine utilization
df['machine_util'] = pd.read_csv(
    "./raw_data/Machine utilization.csv", usecols=['Time%'], sep=';')

# create dataframe for each machine
df_b = df[df['machine_id'] == 'L1 - VPM B (4958)']
df_a = df[df['machine_id'] == 'L2 - VPM A (4959)']
df_c = df[df['machine_id'] == 'L3 - VPM C (4960)']
df_d = df[df['machine_id'] == 'L4 - VPM D (4961)']

# create csv file from each machine dataframe
with open('./aggregate_data/aggregate_data_b.csv', 'a') as f:
    df_b.to_csv(f, header=True, sep=';')

with open('./aggregate_data/aggregate_data_a.csv', 'a') as f:
    df_a.to_csv(f, header=True, sep=';')

with open('./aggregate_data/aggregate_data_c.csv', 'a') as f:
    df_c.to_csv(f, header=True, sep=';')

with open('./aggregate_data/aggregate_data_d.csv', 'a') as f:
    df_d.to_csv(f, header=True, sep=';')
