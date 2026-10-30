import numpy as np
import pandas as pd
from collections import Counter, defaultdict
# np.random.seed(0)

# function from: https://www.iditect.com/faq/python/how-to-round-a-number-to-significant-figures-in-python.html
def round_to_sf(number, sf):
    # Convert the number to a string with the desired number of significant figures
    formatted_number = "{:.{}g}".format(number, sf)
    # Convert the formatted string back to a floating-point number
    rounded_number = float(formatted_number)
    return rounded_number

rng = np.random.default_rng()
# 2 cuts per 1000 miles (1609km) per year - parameterised into per hour for cut statistic
cut_statistic =  (2/1609.344)/8760
# total length of fibre in network in km!!!
network_total_fibre = 5089  

print(round_to_sf(network_total_fibre*cut_statistic,3))