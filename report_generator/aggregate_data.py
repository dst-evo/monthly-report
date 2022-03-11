import pandas as pd

# create empty dataframe to be filled with data
df = pd.DataFrame()

# Read date
df['date'] = pd.read_csv("./data/Produced Boxes.csv",
                         usecols=['DateTime'], sep=';')

# Read machine ID
df['machine_id'] = pd.read_csv("./data/Produced Boxes.csv",
                               usecols=['Machine'], sep=';')

# Read produced boxes
df['produced_boxes'] = pd.read_csv("./data/Produced Boxes.csv",
                                   usecols=['Boxes'], sep=';')

# Read relative and absolute bad boxes
df['rel_bad_boxes'] = pd.read_csv(
    "./data/Bad Boxes.csv", usecols=['Boxes%'], sep=';')
df['abs_bad_boxes'] = pd.read_csv(
    "./data/Bad Boxes.csv", usecols=['Quantity'], sep=';')

# Read run time
df['run_time'] = pd.read_csv("./data/Run Time.csv", usecols=['Hours'], sep=';')

# Read idle time
df['idle_time'] = pd.read_csv(
    "./data/Idle Time.csv", usecols=['Hours'], sep=';')

# Read error time
df['error_time'] = pd.read_csv(
    "./data/Error Time.csv", usecols=['Hours'], sep=';')

# Read corrective maintenance time
df['corr_maint_time'] = pd.read_csv(
    "./data/Corrective Maintenance Time.csv", usecols=['Hours'], sep=';')

# Read preventive maintenance time
df['prev_maint_time'] = pd.read_csv(
    "./data/Preventive Maintenance Time.csv", usecols=['Hours'], sep=';')

# Read operational machine availability
df['op_avail'] = pd.read_csv(
    "./data/Machine availability.csv", usecols=['Time%'], sep=';')
# Read technical machine availability
df['tech_avail'] = pd.read_csv(
    "./data/Machine availability tech.csv", usecols=['Time%'], sep=';')
# Read machine throughput
df['machine_tp'] = pd.read_csv(
    "./data/Machine throughput.csv", usecols=['Boxes/hour'], sep=';')

# Read theoretical machine throughput
df['machine_tp_cmc'] = pd.read_csv(
    "./data/Machine throughput CMC.csv", usecols=['Boxes/hour'], sep=';')

# Read machine utilization
df['machine_util'] = pd.read_csv(
    "./data/Machine utilization.csv", usecols=['Time%'], sep=';')

# write dataframe to csv
with open('collected_data.csv', 'a') as f:
    df.to_csv(f, header=True, sep=';')
