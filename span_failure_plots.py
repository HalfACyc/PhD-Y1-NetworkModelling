# do all the plotting here - the data is generated in span_failure, the data is plotted here.

import matplotlib.pyplot as plt
from span_failure import *
import pandas as pd

def bw_failure_prob_plot(G, df, topology):
    plt.scatter(df['edge_betweenness'], df['failure_prob'], color='#1973EB', marker='x',
                        # label='BT Core',
                        zorder=2)

    title_text = topology+' link properties: edge betweenness vs failure probability'
    plt.grid(which='both', alpha=0.5, zorder=-1)
    plt.title(title_text)
    plt.xlabel('Edge betweenness')
    plt.ylabel('Failure probability')

    # for i, label in enumerate(df['edge_id']):
    #     plt.annotate(label, (df['edge_betweenness'], df['failure_prob']))

    for _, row in df.iterrows():
        plt.annotate(
            row['edge_id'],
            (row['edge_betweenness'], row['failure_prob']),
            textcoords="offset points",
            xytext=(-2, 2),      # nudge label off the marker
            fontsize=8,
            ha='left',
            va='bottom',
        )

    # plt.legend(loc="lower right")
    plt.tight_layout()
    plt.show()


# def betweenness_plots(G, pos, h_or_v):

#     edge_betweenness = nx.edge_betweenness_centrality(G, weight='weight')
#     edge_betweeness_list = []
#     for item in edge_betweenness:
#         edge_betweeness_list.append(edge_betweenness[item])
    
#     nx.draw(G, pos, with_labels=True, node_color='#E0B9AF')

#     edges = nx.draw_networkx_edges(
#         G, pos,
#         edge_color=edge_betweeness_list,
#         width=2.0,
#         edge_cmap=plt.cm.summer)


#     vmin2 = min(edge_betweeness_list)
#     vmax2 = max(edge_betweeness_list)
#     sm2 = plt.cm.ScalarMappable(cmap=plt.cm.summer, norm=plt.Normalize(vmin=vmin2, vmax=vmax2))
#     sm2.set_array([]) 
#     # cbar = plt.colorbar(sm, ax=plt.gca(), label='Betweenness Centrality')
#     plt.colorbar(edges, label='Edge Betweenness Centrality', shrink=0.5, orientation=h_or_v)
#     plt.show()


def betweenness_plots(G, pos, h_or_v, df):
    # Create a lookup dictionary keyed by (node_u, node_v) -> row
    edge_info = {
        (row.node_u, row.node_v): row
        for row in df.itertuples(index=False)
    }
    # Handle the case where edges in G may be in (v, u) order relative to df
    def lookup(u, v):
        return edge_info.get((u, v)) or edge_info.get((v, u))

    # Get betweenness values in the same order nx.draw_networkx_edges uses
    edge_list = list(G.edges())
    edge_betweeness_list = []
    for u, v in edge_list:
        row = lookup(u, v)
        edge_betweeness_list.append(row.edge_betweenness)

    nx.draw(G, pos, with_labels=True, node_color='#E0B9AF')

    edges = nx.draw_networkx_edges(
        G, pos,
        edge_color=edge_betweeness_list,
        width=2.0,
        edge_cmap=plt.cm.summer)

    # Build edge labels: 'id: X\nw: Y'
    edge_labels = {}
    for (u, v) in edge_list:
        row = lookup(u, v)
        # edge_labels[(u, v)] = f"id:{row.edge_id}\nw:{row.length_km:.2f}"
        edge_labels[(u, v)] = f"id:{row.edge_id}"

    nx.draw_networkx_edge_labels(
        G, pos,
        edge_labels=edge_labels,
        font_color='black',
        font_size=7,
        bbox=dict(alpha=0.0, edgecolor='none')  # transparent background
    )

    vmin2 = min(edge_betweeness_list)
    vmax2 = max(edge_betweeness_list)
    plt.colorbar(edges, label='Edge Betweenness Centrality',
                 shrink=0.5, orientation=h_or_v)
    plt.show()


# x = 1
# if x == 1:
#     G, pos = NSFNET()
#     topology = 'NSFNET'
#     orientation = 'horizontal'
# else:
#     G, pos = BT_core()
#     topology = 'BT Core'
#     orientation = 'vertical'

# df = df_failure_prob_bw(G)
# bw_failure_prob_plot(G, df, topology)
# print(df)


# total_fibre = df['length_km'].sum()
# print(total_fibre)


# betweenness_plots(G, pos, orientation, df)

# draws the graphs as MST (bipartite representation) + remaining edges as green dashed curves
def MST_Rep(graph):
    if graph == 1:
        G = NSFNET()[0]
        pos1 = {
                '1':  np.array([0.5 , 1.0]),
                '3':  np.array([0.5 , 0.8]), 
                '4':  np.array([0.5 , 0.6]),  
                '6':  np.array([0.5 , 0.4]), 
                '7':  np.array([0.5 , 0.2]), 
                '9':  np.array([0.5 , 0]),
                '11': np.array([0.5 , -0.2]),  
                '14': np.array([0.5 , -0.4]),
                '2':  np.array([ 1.5, 0.9]),  
                '5':  np.array([ 1.5, 0.7]),   
                '8':  np.array([ 1.5, 0.5]),  
                '10': np.array([ 1.5, 0.3]),
                '12': np.array([ 1.5, 0.1]),  
                '13': np.array([ 1.5, -0.1]),  
            }
    else:
        G = BT_core()[0]
        pos1 = {
            '1':  np.array([0.5 , 1.0]),
            '4':  np.array([0.5 , 0.8]), 
            '5':  np.array([0.5 , 0.6]),   
            '7':  np.array([0.5 , 0.4]), 
            '9':  np.array([0.5 , 0.2]),
            '10': np.array([0.5 , 0.0]),
            '15': np.array([0.5 , -0.2]),
            '19': np.array([0.5 , -0.4]),
            '21': np.array([0.5 , -0.6]),
            '22': np.array([0.5 , -0.8]),

            '2':  np.array([1.5 , 1.3]),  
            '3':  np.array([1.5 , 1.1]), 
            '6':  np.array([1.5 , 0.9]), 
            '8':  np.array([1.5 , 0.7]),  
            '11': np.array([1.5 , 0.5]),  
            '12': np.array([1.5 , 0.3]),  
            '13': np.array([1.5 , 0.1]),  
            '14': np.array([1.5 , -0.1]),
            '16': np.array([1.5 , -0.3]),
            '17': np.array([1.5 , -0.5]),
            '18': np.array([1.5 , -0.7]),
            '20': np.array([1.5 , -0.9]),
            }

        #G, pos = BT_core()

    T = nx.minimum_spanning_tree(G)

    print(list(G.edges))
    print()
    print(list(T.edges))
    print()

    for edge in list(T.edges):
        # print(edge)
        G.remove_edge(edge[0],edge[1])

    print(list(G.edges))

    nx.draw(T, pos1, with_labels=True, node_color='#E0B9AF')
    nx.draw_networkx_edges(G, pos1,connectionstyle="arc3,rad=0.4", arrows=True,
                           edge_color="#3EA71B",
                           style='dashed')
    plt.show()

MST_Rep(2)