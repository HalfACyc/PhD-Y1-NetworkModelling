"""using the prediction vs observation data generated in network_sim_analyse3.py (data stored
in the file 'Simulation-Predictions-UPDATED.csv', plot the predictions vs observations, first for 100 
instances and then again for 1000 instances. compare visually to the x=y line
Yet to do this but also want to return the RMSE of the fit to the y=x line)"""

import pandas as pd 
import matplotlib.pyplot as plt
import numpy as np

# used some code from https://stackoverflow.com/questions/25497402/adding-y-x-to-a-matplotlib-scatter-plot-if-i-havent-kept-track-of-all-the-data

sim_file = 'Blocking_Network_Connectedness_data.csv'

df = pd.read_csv(sim_file)

print(df)

plot = 'comparison'


# plt.figure(figsize=(8, 6))
plt.figure(figsize=(7, 6))

plt.scatter(df['norm_eigen2ndsmallest'], df['observation using 1E5'], color='#1973EB', marker='x',
                label='Observation vs. Prediction', zorder=2)

plt.grid(which='both', alpha=0.5, zorder=-1)

title_text = 'Comparison of NBP 1e-5 and algebraic connectivity of networks'

obs = r'$10^{5}$'
plt.title(title_text)
plt.xlabel('Algebraic connectivity of graph')
plt.ylabel('Number of demands serviced corresponding to NBP 1e-5')
x_lim = plt.xlim()
y_lim = plt.ylim()
# Find the overall min and max across both axes
min_val = min(x_lim[0], y_lim[0])
max_val = max(x_lim[1], y_lim[1])
# plt.plot([min_val, max_val], [min_val, max_val], 'r--', label='y=x',zorder=1)
plt.legend(loc="lower right")
plt.tight_layout()
plt.show()
