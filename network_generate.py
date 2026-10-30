import networkx as nx
import os
from geopy.distance import geodesic as GD
import numpy as np
import matplotlib.pyplot as plt

def betweenness_colours(G, pos):
    node_betweenness = nx.betweenness_centrality(G, weight='weight')
    print(node_betweenness)
    node_betweeness_list = []
    for item in node_betweenness:
        node_betweeness_list.append(node_betweenness[item])
    # for node, centrality in node_betweenness.items():
    #     print(f"Node {node}: {centrality:.4f}")

    edge_betweenness = nx.edge_betweenness_centrality(G, weight='weight')
    edge_betweeness_list = []
    for item in edge_betweenness:
        edge_betweeness_list.append(edge_betweenness[item])
    
    nx.draw(G, pos, with_labels=True, node_color=node_betweeness_list,cmap = plt.cm.summer)
    nodes = nx.draw_networkx_nodes(
    G, pos, 
    node_color=node_betweeness_list, 
    cmap=plt.cm.summer, 
    node_size=300)

    edges = nx.draw_networkx_edges(
        G, pos,
        edge_color=edge_betweeness_list,
        width=2.0,
        edge_cmap=plt.cm.copper)

    vmin1 = min(node_betweeness_list)
    vmax1 = max(node_betweeness_list)
    sm1 = plt.cm.ScalarMappable(cmap=plt.cm.summer, norm=plt.Normalize(vmin=vmin1, vmax=vmax1))
    sm1.set_array([]) 

    vmin2 = min(edge_betweeness_list)
    vmax2 = max(edge_betweeness_list)
    sm2 = plt.cm.ScalarMappable(cmap=plt.cm.copper, norm=plt.Normalize(vmin=vmin2, vmax=vmax2))
    sm2.set_array([]) 
    # cbar = plt.colorbar(sm, ax=plt.gca(), label='Betweenness Centrality')
    plt.colorbar(nodes, label='Node Betweenness Centrality', shrink=0.5, orientation="horizontal")
    plt.colorbar(edges, label='Edge Betweenness Centrality', shrink=0.5, orientation="horizontal")
    plt.show()


def NSFNET():
    G = nx.Graph()
    G.add_edge('1', '2', weight = 2100)
    G.add_edge('1', '3', weight = 3000)
    G.add_edge('1', '8', weight = 4800)
    G.add_edge('2', '4', weight = 1500)
    G.add_edge('2', '3', weight = 1200)
    G.add_edge('3', '6', weight = 3600)
    G.add_edge('4', '5', weight = 1200)
    G.add_edge('4', '11', weight = 3900)
    G.add_edge('5', '6', weight = 2400)
    G.add_edge('5', '7', weight = 1200)
    G.add_edge('6', '10', weight = 2100)
    G.add_edge('6', '14', weight = 3600)
    G.add_edge('7', '8', weight = 1500)
    G.add_edge('7', '10', weight = 2700)
    G.add_edge('8', '9', weight = 1500)
    G.add_edge('9', '10', weight = 1500)
    G.add_edge('9', '12', weight = 600)
    G.add_edge('9', '13', weight = 600)
    G.add_edge('11', '12', weight = 1200)
    G.add_edge('11', '13', weight = 1500)
    G.add_edge('12', '14', weight = 600)
    G.add_edge('13', '14', weight = 300)

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
    '14': np.array([2.40, 0.65])
    }
    betweenness_colours(G, pos)

def BT_core():
    # node 1 and 7 are not for supplying or receiving traffic
    # they are for routing purposes only
    G = nx.Graph()
    G.add_edge('1', '2', weight = 120)
    G.add_edge('1', '3', weight = 240)
    G.add_edge('1', '5', weight = 182)
    G.add_edge('2', '4', weight = 686)
    G.add_edge('2', '7', weight = 163)
    G.add_edge('3', '4', weight = 48)
    G.add_edge('4', '6', weight = 419)
    G.add_edge('5', '6', weight = 109)
    G.add_edge('5', '8', weight = 62)
    G.add_edge('6', '7', weight = 87)
    G.add_edge('6', '9', weight = 99)
    G.add_edge('7', '11', weight = 275)
    G.add_edge('8', '9', weight = 75)
    G.add_edge('8', '14', weight = 160)
    G.add_edge('9', '12', weight = 73)
    G.add_edge('10', '11', weight = 105)
    G.add_edge('10', '12', weight = 163)
    G.add_edge('10', '16', weight = 127)
    G.add_edge('11', '17', weight = 183)
    G.add_edge('12', '15', weight = 89)
    G.add_edge('13', '16', weight = 23)
    G.add_edge('13', '17', weight = 7)
    G.add_edge('13', '19', weight = 5)
    G.add_edge('14', '15', weight = 27)
    G.add_edge('14', '20', weight = 439)
    G.add_edge('15', '18', weight = 203)
    G.add_edge('15', '20', weight = 234)
    G.add_edge('16', '19', weight = 20)
    G.add_edge('17', '19', weight = 2)
    G.add_edge('17', '22', weight = 115)
    G.add_edge('18', '21', weight = 197)
    G.add_edge('18', '22', weight = 55)
    G.add_edge('20', '21', weight = 71)
    G.add_edge('21', '22', weight = 226)

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

    betweenness_colours(G, pos)

current_dir = os.getcwd()
print("Current Directory:", current_dir)
# Change to a new directory (modify the path as per your system)
TopZoo_folder = current_dir + "\\TopologyZooGraphs"
os.chdir(TopZoo_folder) 

"""This function examines each network from Internet Topology Zoo and 
sifts them in stages based on the following parameters:
Stage 1: check if the size of the network is appropriate (smaller than 26 nodes)
Stage 2: check if every node has latitude and longitude data
Stage 3: check if every node is connected to the rest of the graph
"""
# sift 
def files_sift():
    # list of files in folder
    dir_list = os.listdir(TopZoo_folder)
    # list of files that don't have lat/long data
    stage1_sift = []
    stage2_sift = []
    stage3_sift = []
    rejected = []

    for graph in dir_list:
        G = nx.read_graphml(graph)
        # stage 1 sift
        if G.number_of_nodes() >= 26:
            rejected.append(graph)
            stage1_sift.append(graph)
            continue
        stage1_sift.append(graph)
        
        # stage 2 sift
        missing_coords = False
        for node, data in G.nodes(data=True):
            # Check if both Latitude and Longitude exist in node attributes
            if 'Latitude' not in data or 'Longitude' not in data:
                missing_coords = True
                break
        if missing_coords:
            rejected.append(graph)
            continue
        stage2_sift.append(graph)

        # stage 3 sift
        if not nx.is_connected(G):
            # Get number of connected components
            num_components = nx.number_connected_components(G)
            rejected.append((graph, f"Graph is not connected. Has {num_components} components"))
            continue
        stage3_sift.append(graph)

    return(stage3_sift)

# returns the name and unweighted, undirected graph
# used in laplacian eigenvalue analysis 
def return_graph(graph_name):
    G = nx.read_graphml(graph_name)
    top_name = graph_name.split('.')[0]
    return(G, top_name)

# takes a graph's edges and works out weights by calculating shortest distance between nodes using lat/long data
# returns the resulting weighted graph itself and its name
def graph_weightify(graph_name):
    G = nx.read_graphml(graph_name)
    top_name = graph_name.split('.')[0]

    # if there are parallel edges (two edges between same node pair) then collapse them into a simple graph
    if G.is_multigraph():
        G = nx.Graph(G)

    nodes_dict = dict(G.nodes(data=True))
    edges_lst = list(G.edges())

    for edge in edges_lst:
        coords = []
        for node in edge:
            node_data = nodes_dict[node]
            lat = node_data['Latitude']
            long = node_data['Longitude']
            coords.append((lat, long))
        distance = round(GD(coords[0],coords[1]).km)

        # tweak distances to include extra provisioning for real life laying/obstacles/elevation change
        if distance <= 1000:
            link = 1.5 * distance
        elif 1000 < distance <= 1200:
            link = 1500
        else:
            link = 1.25 * distance
        G.edges[edge]['weight'] = link
    return(G, top_name)

G = NSFNET()
# G = BT_core()

