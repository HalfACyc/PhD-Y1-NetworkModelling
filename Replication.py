# from span_failure import *
# import pandas as pd

# G = NSFNET()[0]
# # Number of instances in simulation. 
# simulation_size = 8760
# no_edges = len(list(G.edges()))

# # interval length of time corresponding to one instance, in hours  
# interval = 1
# # 
# time_period = 8760/interval
# # link_fail_prob = 2/1609.3

# df = nx.to_pandas_edgelist(G)
# df["link_failure_p"] = df["weight"] * (2/1609.3) / time_period

# print(df)

# link_downtime_record = []
# links_down = []

# for instance in simulation_size:



# # for edges in list(G.edges(data=True)):
# #     print(edges)



import numpy as np

no_years = 1

rng = np.random.default_rng()
lam, size = 0.00604, 8760*no_years
s = rng.poisson(lam=lam, size=size)
#print(s)
unique, counts = np.unique(s, return_counts=True)
occurrences = dict(zip(unique, counts))
print(occurrences)

downtime = {}

for item in occurrences:
    if item != 0:

        # print("All index value of %s is: "%item, np.where(s == item)[0])
        downtime[item] = np.where(s == item)
# print(s.mean(), s.var())


print(downtime)
# repair_1 = np.random.randint(low=6, high=10, size=)