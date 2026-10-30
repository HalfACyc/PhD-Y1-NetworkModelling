"""using the prediction vs observation data generated in network_sim_analyse3.py (data stored
in the file 'Simulation-Predictions-UPDATED.csv', plot the predictions vs observations, first for 100 
instances and then again for 1000 instances. compare visually to the x=y line
Yet to do this but also want to return the RMSE of the fit to the y=x line)"""

import pandas as pd 
import matplotlib.pyplot as plt
import numpy as np

# used some code from https://stackoverflow.com/questions/25497402/adding-y-x-to-a-matplotlib-scatter-plot-if-i-havent-kept-track-of-all-the-data

sim_file = 'Simulation-Predictions-10e-6using10e4and10e5.csv'

df = pd.read_csv(sim_file)

print(df)

plot = 'comparison'


# plt.figure(figsize=(8, 6))
# plt.figure(figsize=(7, 6))

fig, ax = plt.subplots(figsize=(14, 8))

plt.scatter(df['Topology'], df['prediction using 1e4'], color='#1973EB', marker='x',
                label='prediction of 1e-6 using 1e4', zorder=2)


plt.scatter(df['Topology'], df['prediction using 1e5'], color="#FF0000", marker='x',
                label='prediction of 1e-6 using 1e5', zorder=2)

differences = df['prediction using 1e5'] - df['observation of 1e-4 using 1e5']


# Add difference labels above each bar
for i, (x, diff) in enumerate(zip(df['Topology'], differences)):
    # Position the text above the taller of the two values (bar or scatter1)
    y_pos = max(df['prediction using 1e5'][i], df['observation of 1e-4 using 1e5'][i]) + 0.5
    
    # Color code: positive difference in blue, negative in orange
    color = 'blue' if diff >= 0 else 'darkorange'
    
    ax.text(x, y_pos, f'{diff:+.2f}', 
            ha='center', va='bottom', 
            fontsize=7, color=color, fontweight='bold',
            rotation=90)  # Rotate for readability with 38 items


width = 0.6
x = np.arange(len(df['Topology']))
bars_up = ax.bar(x, df['observation of 1e-4 using 1e5'], width, 
                 color='steelblue', alpha=0.4, label='observation of 1e-4 using 1e5')

plt.grid(which='both', alpha=0.5, zorder=-1)



title_text = 'Comparison of number of demands serviced within four 9s reliability (observed)\nto six 9s reliability (predicted)'

obs = r'$10^{5}$'
plt.title(title_text, fontsize=16)
# plt.xlabel('Prediction using %s instances'%(no_seeds), fontsize=20)
# plt.ylabel('Observation using %s instances'%(obs), fontsize=20)
x_lim = plt.xlim()
y_lim = plt.ylim()
# Find the overall min and max across both axes
min_val = min(x_lim[0], y_lim[0])
max_val = max(x_lim[1], y_lim[1])
ax.set_xlabel('Topology',fontsize=14)
ax.set_ylabel('No. of Demands Serviced',fontsize=14)
ax.set_xticklabels(df['Topology'], rotation=45, ha='right')
# plt.plot([min_val, max_val], [min_val, max_val], 'r--', label='y=x',zorder=1)
plt.legend(loc="upper right")
plt.tight_layout()
# plt.show()
filename = '2.png'
plt.savefig(filename)
plt.close()
