import pickle
import os
import numpy as np

current_dir = os.getcwd()
dir_list = os.listdir(current_dir)

pickle_files = []
for file in dir_list:
    if '.pkl' in file:
        pickle_files.append(file)


file = pickle_files[1]


file_data = file.split('-')
topology = file_data[0]
years = file_data[1]
seeds = file_data[3]

with open(file, "rb") as file:
    d = pickle.load(file)

# print(d)
print(topology)
for no_failures in d:
    # print(d[no_failures])
    scaled_data = np.array(d[no_failures]) / int(years)
    # print(scaled_data)
    print('number of concurrent failures:', no_failures)
    print('number of seeds present in:',len(scaled_data))
    print('mean:',np.mean(scaled_data))
    print('variance:',np.var(scaled_data))
    print()