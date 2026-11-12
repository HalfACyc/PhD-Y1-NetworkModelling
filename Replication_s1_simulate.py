import numpy as np
import pandas as pd
from collections import Counter, defaultdict
import pickle
import math

# function from: https://www.iditect.com/faq/python/how-to-round-a-number-to-significant-figures-in-python.html
def round_to_sf(number, sf):
    # Convert the number to a string with the desired number of significant figures
    formatted_number = "{:.{}g}".format(number, sf)
    # Convert the formatted string back to a floating-point number
    rounded_number = float(formatted_number)
    return rounded_number

all_results = {1:[],2:[],3:[],4:[],5:[]}
years = 1000
seeds = 50
# 2 cuts per 1000 miles (1609km) per year - parameterised into per hour for cut statistic
cut_statistic =  (2/1609.344)/8760
# failure rate of amplifiers, 2000 cuts every 10^9 hours. Parameterised per hour
amp_fail_statistic = 2000/(10**9)
# total length of fibre in network in km!!!

# topology = 'Ref3'
# network_total_fibre = 25200  
# topology = 'BT_Core'
topology = 'NSFNET'
network_total_fibre = 42600  

# assume span length is 100km, find an upper bound on the number of amplifiers needed
no_amps = math.ceil(network_total_fibre/100)

for seed in range(seeds):
    np.random.seed(seed)
    rng = np.random.default_rng()

    # incidents of cut fibre
    lam, size = round_to_sf(network_total_fibre*cut_statistic,3), 8760*years
    cut_incidents = rng.poisson(lam=lam, size=size)

    lam2, size2 = round_to_sf(no_amps*amp_fail_statistic,3), 8760*years
    amp_incidents = rng.poisson(lam=lam2, size=size2)

    unique, counts = np.unique(cut_incidents, return_counts=True)
    unique2, counts2 = np.unique(amp_incidents, return_counts=True)

    occurrences_cut = dict(zip(unique, counts))
    occurrences_amp = dict(zip(unique2, counts2))
    # print('occurrences',occurrences)

    cut_instance = {}
    amp_instance = {}

    # indexes of the fibre cut are stored as the value in this dictionary
    for item in occurrences_cut:
        if item != 0:
            cut_instance[item] = np.where(cut_incidents == item)[0].tolist()

    # indexes of the amp failure are stored as the value in this dictionary
    for item in occurrences_amp:
        if item != 0:
            amp_instance[item] = np.where(amp_incidents == item)[0].tolist()

    # Every hour that a link is down (per link) is written to list 'all_down_links'
    # Repeated hours indicate multiple links down at the same instance.
    all_down_links = []
    for item in cut_instance:
        for repeat in range(item):
            # repair times are actually 6-10 hours but written as 5 to 9 because the instance it breaks is counted as an hour.
            repair = np.random.randint(low=5, high=9, size=len(cut_instance[item]))
            # print(item, repair)
            for i in range(len(repair)):
                all_down_links += [num for num in range(
                    cut_instance[item][i], cut_instance[item][i]+repair[i] + 1)
                    ] 

    for item in amp_instance:
        for repeat in range(item):
            # repair times are actually 6-10 hours but written as 5 to 9 because the instance it breaks is counted as an hour.
            repair = np.random.randint(low=2, high=4, size=len(amp_instance[item]))
            # print(item, repair)
            for i in range(len(repair)):
                all_down_links += [num for num in range(
                    amp_instance[item][i], amp_instance[item][i]+repair[i] + 1)
                    ] 


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
file_name = topology + '-'+ str(years)+'-years-'+str(seeds)+'-seeds-plusamps.pkl'
results_file = open(file_name, 'wb')
pickle.dump(all_results, results_file)
results_file.close()