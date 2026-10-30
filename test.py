import numpy as np
import pandas as pd
from collections import Counter, defaultdict
np.random.seed(0)

rng = np.random.default_rng()
lam, size = 0.00604, 8760
incidents = np.array([0, 2, 0, 1, 0, 0, 1, 0, 0, 0])
#print(s)
unique, counts = np.unique(incidents, return_counts=True)
occurrences = dict(zip(unique, counts))
print('occurrences',occurrences)

fault_instance = {}

for item in occurrences:
    if item != 0:

        # print("All index value of %s is: "%item, np.where(s == item)[0])
        fault_instance[item] = np.where(incidents == item)[0].tolist()
# print(s.mean(), s.var())


print('fault_instance:', fault_instance)

# for item in downtime:
    # repair_temp = np.random.randint(low=6, high=10, size=)
# 4 hours, 2 hours and 3 hours respectively. -1 because this then accounts for the hour it breaks, too
repair_duration = {} 

all_down_links = []
for item in fault_instance:
    for repeat in range(item):
        repair = np.random.randint(low=2, high=4, size=len(fault_instance[item]))
        print(item, repair)
        for i in range(len(repair)):
            all_down_links += [num for num in range(
                fault_instance[item][i], fault_instance[item][i]+repair[i] + 1)
                ] 

# every instance when a link is down, concurrently
print(all_down_links)


result = defaultdict(list)
for num, count in Counter(all_down_links).items():
    result[count].append(num)

result = dict(result)
print(result)
# repaired_time = fault_instance[1] + repair_duration


# print('repaired by:', repaired_time)
# # repair = np.random.randint(low=6, high=10, size=)
# # repair = 

# print('Temp list')
# all_down_links = []
# for i in range(len(repaired_time)):
#     print(fault_instance[1][i])
#     print(repaired_time[i])
#     all_down_links += [num for num in range(fault_instance[1][i], repaired_time[i] + 1)]
# print(all_down_links)

# all_down_links = np.array(all_down_links)


# result = defaultdict(list)
# for num, count in Counter(all_down_links).items():
#     result[count].append(num)

# result = dict(result)
# print(result)

# # print()
# # print()

# # unique1, counts1 = np.unique(all_down_links, return_counts=True)
# # new = dict(zip(unique1, counts1))

# # print(new)
# # df = pd.DataFrame(list(new.items()), columns=['hour', 'links_down'])
# # print(df)


