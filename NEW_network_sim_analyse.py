"""This file makes predictions and takes observations of the number of transmissions until 
block for each network. For each network, make predictions of 10^-6 NBP using 10,000 and 100,000 seeds.
No observation data to compare against because simulations too large - even to do 10^6 is too large.
Then save this data to a csv file: 'Simulation-Predictions-higher-order.csv'"""


"""further process the data
This file uses the simulation data and curve fitting to make predictions for smaller blocking probabilities
"""
import pandas as pd 
import os
import numpy as np
from pathlib import Path
from scipy import stats

# truncation proportion - keeping this proportion of smallest data as my lower tail
tail_quantile = 0.30 

current_dir = os.getcwd()
print("Current Directory:", current_dir)

data_folder = current_dir + "\\net4csv_files"
os.chdir(data_folder)
dir_list = os.listdir(data_folder)


def gpd_quantile(y, threshold, prob_le_threshold, shape_gpd, scale_gpd):
    """
    Inverse CDF for the lower‑tail GPD model.
    Returns x such that P(X <= x) = y, for y <= prob_le_threshold.
    """
    if y > prob_le_threshold:
        # Requested probability exceeds the threshold probability – return threshold
        return threshold
        # Solve: y = prob_le_threshold * (1 - GPD_cdf(threshold - x))
    # => threshold - x = GPD_ppf(1 - y / prob_le_threshold)
    u = 1.0 - y / prob_le_threshold
    # u is in [0,1]. GPD ppf with loc=0.
    exceedance = stats.genpareto.ppf(u, shape_gpd, loc=0, scale=scale_gpd)
    x = threshold - exceedance
    # Ensure x is not negative (transmission counts cannot be < 0)
    return max(x, 0.0)


# this function takes the data file and returns the value for the closest target probability
def give_file_value(file, target_prob):
    df = pd.read_csv(file)
    
    idx = (df['Probability'] - target_prob).abs().idxmin()
    txs_value = df.loc[idx, 'Txs until block']

    # raw_obs = df['Txs until block'].values
    # y_emp = df['Probability'].values
    return(txs_value)


def curve_fit_return_val(file,target_prob):
    parameters = file.split('-')
    topology = parameters[1]
    no_seeds = int(parameters[5])

    df = pd.read_csv(file)
    raw_obs = df['Txs until block'].values

    threshold = np.percentile(raw_obs, tail_quantile * 100)
    # fit GPD to exceedances
    tail_data = raw_obs[raw_obs <= threshold]
    exceedances = threshold - tail_data  
    shape_gpd, loc_gpd, scale_gpd = stats.genpareto.fit(exceedances, floc=0)
    prob_le_threshold = (raw_obs <= threshold).mean()

    # Target cumulative probabilities (y values)
    x_val = gpd_quantile(target_prob, threshold, prob_le_threshold, shape_gpd, scale_gpd)
    fitted_quantile = round(x_val, 1)
    return(fitted_quantile)


graph_names_lst = []
for file in dir_list:
    parameters = file.split('-')
    name = parameters[1]
    if name not in graph_names_lst:
        graph_names_lst.append(name)

# remove the following graphs because they have dodgy Q-Q plots (and weird fitting)
removal = ('Arpanet19706', 'Arpanet196912','Dataxchange',
    'Epoch', 'Gblnet', 'Getnet', 'Heanet', 'Itnet', 'KentmanJul2005',
    'Kreonet','Layer42','Mren','Napnet','Netrail',
    'Noel','NSFNET','Psinet','Sanren','Telecomserbia')

target_probs = [1e-5,1e-6]
# target_probs = [1e-3, 1e-4, 1e-5, 1e-6, 1e-7]
# target_probs_str = list(map(str, target_probs))

col_names = ['Topology','prediction using 1e4','prediction using 1e5']

# col_names = ['Topology','no. seeds','threshold'] + target_probs_str

curve_data_df = pd.DataFrame(columns = col_names)


# predictions using 100(1E2) and 1000(1E3) seeds of 1e-4, and observation of 1e-4 using 1e5 seeds
graph_names_lst = [e for e in graph_names_lst if e not in removal]
for graph in graph_names_lst:
    data = {
        'Topology':graph,
        'prediction using 1e4':0,
        'prediction using 1e5':0
    }
    # extract the relevant simulation files for a given graph
    graph_files = list(filter(lambda x: graph in x, dir_list))
    print(graph_files)
    for file in graph_files:
        no_seeds = file.split('-')[5]
        if str(no_seeds) == str(10000):
            data10000 = curve_fit_return_val(file,1e-6)
            print(data10000)
            data['prediction using 1e4'] = data10000
        elif str(no_seeds) == str(100000):
            data100000 = curve_fit_return_val(file,1e-6)
            print(data100000)
            data['prediction using 1e5'] = data100000
    curve_data_df.loc[len(curve_data_df)] = data

    print()

        
print(curve_data_df)

filename = 'Simulation-Predictions-higher-order.csv'
current_dir = Path.cwd()
parent_dir = current_dir.parent  

full_path = parent_dir / filename

curve_data_df.to_csv(full_path, index=False)