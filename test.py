import numpy as np

rng = np.random.default_rng()
lam, size = 0.00604, 8760
incidents = np.array([0, 1, 0, 1, 0, 0, 1, 0, 0, 0])
#print(s)
unique, counts = np.unique(incidents, return_counts=True)
occurrences = dict(zip(unique, counts))
print(occurrences)

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
repair_duration = np.array([3, 1, 2])

repaired_time = fault_instance[1] + repair_duration


print('repaired by:', repaired_time)
# repair = np.random.randint(low=6, high=10, size=)
# repair = 

print('Temp list')
all_down_links = []
for i in range(len(repaired_time)):
    print(fault_instance[1][i])
    print(repaired_time[i])
    all_down_links += [num for num in range(fault_instance[1][i], repaired_time[i] + 1)]
print(all_down_links)



