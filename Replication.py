import numpy as np
import pandas as pd
from collections import Counter, defaultdict

# function from: https://www.iditect.com/faq/python/how-to-round-a-number-to-significant-figures-in-python.html
def round_to_sf(number, sf):
    # Convert the number to a string with the desired number of significant figures
    formatted_number = "{:.{}g}".format(number, sf)
    # Convert the formatted string back to a floating-point number
    rounded_number = float(formatted_number)
    return rounded_number

all_results = {1:[],2:[],3:[],4:[]}
years = 1000
seeds = 50

for seed in range(seeds):
    np.random.seed(seed)
    rng = np.random.default_rng()
    # 2 cuts per 1000 miles (1609km) per year - parameterised into per hour for cut statistic
    cut_statistic =  (2/1609.344)/8760
    # total length of fibre in network in km!!!
    network_total_fibre = 25200  

    # incidents of cut fibre
    lam, size = round_to_sf(network_total_fibre*cut_statistic,3), 8760*years
    incidents = rng.poisson(lam=lam, size=size)

    #print(s)
    unique, counts = np.unique(incidents, return_counts=True)
    occurrences = dict(zip(unique, counts))
    print('occurrences',occurrences)

    fault_instance = {}

    for item in occurrences:
        if item != 0:

            fault_instance[item] = np.where(incidents == item)[0].tolist()
    # print(s.mean(), s.var())


    # print('fault_instance:', fault_instance)

    # for item in downtime:
        # repair_temp = np.random.randint(low=6, high=10, size=)
    # 4 hours, 2 hours and 3 hours respectively. -1 because this then accounts for the hour it breaks, too
    repair_duration = {} 

    all_down_links = []
    for item in fault_instance:
        for repeat in range(item):
            # repair times are actually 6-10 hours but written as 5 to 9 because the instance it breaks is counted as an hour.
            repair = np.random.randint(low=5, high=9, size=len(fault_instance[item]))
            # print(item, repair)
            for i in range(len(repair)):
                all_down_links += [num for num in range(
                    fault_instance[item][i], fault_instance[item][i]+repair[i] + 1)
                    ] 

    # every instance when a link is down, concurrently
    # print('all_down_links:',all_down_links)


    result = defaultdict(list)
    for num, count in Counter(all_down_links).items():
        result[count].append(num)

    result = dict(result)
    # print('concurrent failures:',result)
    print('concurrent failures:')

    for item in result:
        print(item, len(result[item]))
        all_results[item].append(len(result[item]))

print()
print(all_results)
