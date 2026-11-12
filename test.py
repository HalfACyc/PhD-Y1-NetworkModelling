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

np.random.seed(0)
rng = np.random.default_rng()

lam, size = 3, 1000
cut_incidents = rng.poisson(lam=lam, size=size)

print(cut_incidents)
print(np.count_nonzero(cut_incidents == 1)/1000)
print(np.count_nonzero(cut_incidents == 2)/1000)
print(np.count_nonzero(cut_incidents == 3)/1000)
print(np.count_nonzero(cut_incidents == 4)/1000)
print(np.var(cut_incidents))
print(np.mean(cut_incidents))