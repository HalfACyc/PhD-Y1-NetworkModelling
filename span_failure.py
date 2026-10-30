import math
import networkx as nx
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def round_to_sf(number, sf):
    # Convert the number to a string with the desired number of significant figures
    formatted_number = "{:.{}g}".format(number, sf)
    # Convert the formatted string back to a floating-point number
    rounded_number = float(formatted_number)
    return rounded_number

def BT_core():
    
    # node 1 and 7 are not for supplying or receiving traffic
    # they are for routing purposes only
    G = nx.Graph()
    edges = [('1', '2', 120),('1', '3', 240),('1', '5',  182),('2', '4', 686),
             ('2', '7', 163),('3', '4', 48),('4', '6', 419),('5', '6', 109),
             ('5', '8', 62),('6', '7', 87),('6', '9', 99),('7', '11', 275),
             ('8', '9', 75),('8', '14', 160),('9', '12', 73),('10', '11', 105),
             ('10', '12', 163),('10', '16', 127),('11', '17', 183),('12', '15', 89),
             ('13', '16', 23),('13', '17', 7),('13', '19', 5),('14', '15', 27),
             ('14', '20', 439),('15', '18', 203),('15', '20', 234),('16', '19', 20),
             ('17', '19', 2),('17', '22', 115),('18', '21', 197),('18', '22', 55),
             ('20', '21', 71),('21', '22', 226)
    ]
    for u, v, w in edges:
        G.add_edge(u, v, weight=w)

    pos = {
        '1': np.array([0, 1.4]),
        '2': np.array([1, 1.4]),  
        '3': np.array([0.20, 1.20]), 
        '4': np.array([0.4, 1.2]),  
        '5': np.array([0, 1]),   
        '6': np.array([0.4, 1.00]), 
        '7': np.array([1, 1]), 
        '8': np.array([0, 0.8]),  
        '9': np.array([0.4, 0.8]),
        '10': np.array([0.6, 0.8]),
        '11': np.array([1, 0.80]),  
        '12': np.array([0.4, 0.60]),  
        '13': np.array([0.8, 0.6]),  
        '14': np.array([0, 0.4]),
        '15': np.array([0.4, 0.4]),
        '16': np.array([0.6, 0.4]),
        '17': np.array([1, 0.4]),
        '18': np.array([0.6, 0.2]),
        '19': np.array([0.8, 0.2]),
        '20': np.array([0, 0]),
        '21': np.array([0.4, 0]),
        '22': np.array([1, 0]),
        }
    return(G, pos)

def NSFNET():
    G = nx.Graph()
    edges = [
        ('1','2',2100), ('1','3',3000), ('1','8',4800), ('2','4',1500),
        ('2','3',1200), ('3','6',3600), ('4','5',1200), ('4','11',3900),
        ('5','6',2400), ('5','7',1200), ('6','10',2100), ('6','14',3600),
        ('7','8',1500), ('7','10',2700), ('8','9',1500), ('9','10',1500),
        ('9','12',600), ('9','13',600), ('11','12',1200), ('11','13',1500),
        ('12','14',600), ('13','14',300),
    ]
    for u, v, w in edges:
        G.add_edge(u, v, weight=w)

    pos = {
        '1': np.array([0.20, 1.00]),
        '2': np.array([0.0, 0.60]),  
        '3': np.array([0.20, 0.20]), 
        '4': np.array([0.7, 0.65]),  
        '5': np.array([1.0, 0.55]),   
        '6': np.array([1.20, 0.00]), 
        '7': np.array([1.40, 0.60]), 
        '8': np.array([1.7, 0.55]),  
        '9': np.array([2.1, 0.55]),
        '10': np.array([2.00, 0.15]),
        '11': np.array([1.9, 0.70]),  
        '12': np.array([2.40, 0.80]),  
        '13': np.array([2.60, 0.75]),  
        '14': np.array([2.40, 0.60])
    }
    return(G, pos)

# link and span lengths in km
def link_failure_prob(link_length, span_length = 80, span_failure_prob = 10E-5):
    no_spans = math.ceil(link_length/span_length)

    # link_failure_prob = 1 - math.exp(math.log(1-span_failure_prob))**(no_spans)
    # above formula is fine but the exponential log introduces error
    # simpler expression below:
    link_failure_prob = 1 - (1-span_failure_prob)**(no_spans)

    return(link_failure_prob)


def df_failure_prob_bw(G):
    for u, v, d in G.edges(data=True):
        # edge_failure_prob = round_to_sf(link_failure_prob(d['weight']), 4)
        # unrounded to sf
        edge_failure_prob = link_failure_prob(d['weight'])
        G[u][v]['failure_prob'] = edge_failure_prob

    edge_bw = nx.edge_betweenness_centrality(G, weight='weight')
    for (u, v), bw in edge_bw.items():
        G[u][v]['edge_bw'] = bw

    for i, (u, v) in enumerate(G.edges()):
        G[u][v]['id'] = i

    rows = [
        {
            'edge_id': d['id'],
            'node_u': u,
            'node_v': v,
            'length_km': d['weight'],
            'edge_betweenness': d['edge_bw'],
            'failure_prob': d['failure_prob'],
        }
        for u, v, d in G.edges(data=True)
    ]
    df = pd.DataFrame(rows)
    return(df)



# x = 2

# if x == 1:
#     G, pos = NSFNET()
#     pos1 = {
#             '1':  np.array([0.5 , 1.0]),
#             '3':  np.array([0.5 , 0.8]), 
#             '4':  np.array([0.5 , 0.6]),  
#             '6':  np.array([0.5 , 0.4]), 
#             '7':  np.array([0.5 , 0.2]), 
#             '9':  np.array([0.5 , 0]),
#             '11': np.array([0.5 , -0.2]),  
#             '14': np.array([0.5 , -0.4]),
#             '2':  np.array([ 1.5, 0.9]),  
#             '5':  np.array([ 1.5, 0.7]),   
#             '8':  np.array([ 1.5, 0.5]),  
#             '10': np.array([ 1.5, 0.3]),
#             '12': np.array([ 1.5, 0.1]),  
#             '13': np.array([ 1.5, -0.1]),  
#         }
# else:
#     G, pos = BT_core()
#     pos1 = {
#         '1':  np.array([0.5 , 1.0]),
#         '4':  np.array([0.5 , 0.8]), 
#         '5':  np.array([0.5 , 0.6]),   
#         '7':  np.array([0.5 , 0.4]), 
#         '9':  np.array([0.5 , 0.2]),
#         '10': np.array([0.5 , 0.0]),
#         '15': np.array([0.5 , -0.2]),
#         '19': np.array([0.5 , -0.4]),
#         '21': np.array([0.5 , -0.6]),
#         '22': np.array([0.5 , -0.8]),

#         '2':  np.array([1.5 , 1.3]),  
#         '3':  np.array([1.5 , 1.1]), 
#         '6':  np.array([1.5 , 0.9]), 
#         '8':  np.array([1.5 , 0.7]),  
#         '11': np.array([1.5 , 0.5]),  
#         '12': np.array([1.5 , 0.3]),  
#         '13': np.array([1.5 , 0.1]),  
#         '14': np.array([1.5 , -0.1]),
#         '16': np.array([1.5 , -0.3]),
#         '17': np.array([1.5 , -0.5]),
#         '18': np.array([1.5 , -0.7]),
#         '20': np.array([1.5 , -0.9]),
#         }

#     #G, pos = BT_core()

# T = nx.minimum_spanning_tree(G)

# y=1
# if y!=1:
#     pos = pos1

# nx.draw(T, pos, with_labels=True, node_color='#E0B9AF')
# plt.show()