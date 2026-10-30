"""get normalised eigenvalues of laplacian matrix and determine connectedness
then do a spectral plot of the eigenvalues,"""
import networkx as nx
from network_generate import *
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

all_files = files_sift()

# remove the following graphs because they have dodgy Q-Q plots (and weird fitting)
removal = ('Arpanet19706.graphml', 'Arpanet196912.graphml','Dataxchange.graphml',
    'Epoch.graphml', 'Gblnet.graphml', 'Getnet.graphml', 'Heanet.graphml', 'Itnet.graphml', 'KentmanJul2005.graphml',
    'Kreonet.graphml','Layer42.graphml','Mren.graphml','Napnet.graphml','Netrail.graphml',
    'Noel.graphml','NSFNET.graphml','Psinet.graphml','Sanren.graphml','Telecomserbia.graphml')


all_files = [e for e in all_files if e not in removal]

data = {'Graph name':[], 'norm_eigen2ndsmallest':[], 'dist_to_bipartiteness':[]}
df = pd.DataFrame(data)


def eigenvalue_spectra(eigenvalues, name):
    sigma = 0.01                     # Gaussian kernel width
    norm = 1.0 / (sigma * np.sqrt(2 * np.pi))   # Gaussian normalization factor

    # Define x-axis range (add a small margin)
    x_min = 0 - 0.2
    x_max = 2 + 0.2
    x_grid = np.linspace(x_min, x_max, 1000)

    # Compute f(x) by summing Gaussian contributions from all eigenvalues
    # Vectorized: create a matrix of shape (len(x_grid), len(eigenvalues))
    diff = x_grid[:, None] - eigenvalues      # differences x - lambda_i
    exponent = - (diff ** 2) / (2 * sigma ** 2)
    f = norm * np.sum(np.exp(exponent), axis=1)

    # Plot
    plt.figure(figsize=(7.5, 5.5))
    plt.plot(x_grid, f, 'b-', linewidth=1.5)
    plt.xlabel('Normalised Eigenvalue', fontsize=20)
    plt.ylabel('f(x)', fontsize=20)
    plt.title('%s spectral plot with Gaussian\nkernel convolution (σ = 0.01)'%name, fontsize=20)
    plt.grid(alpha=0.3)
    # plt.show()

    filename = name + '.png'
    plt.savefig(filename)
    plt.close()
    


for file in all_files:
    print(file)
    graph_name = file.split('.')[0]
    # since return_graph is used, just the graph connectivity is provided for analysis
    # i.e. no directivity or weights in the graphs
    generate = return_graph(file)
    G, topology = generate[0], generate[1]
    print()
    # print(G.edges.data())
    n_eigenvalues = nx.normalized_laplacian_spectrum(G)
    np.sort(n_eigenvalues)
    n_eigenvalues = n_eigenvalues.round(3)
    print(', '.join(map(str,n_eigenvalues)))

    # eigenvalue_spectra(n_eigenvalues,graph_name)

    print()
    df.loc[len(df)] = [graph_name, n_eigenvalues[1],(2-n_eigenvalues[-1])]


# print(df.sort_values(by=["norm_eigen2ndsmallest"],ascending=False))
def create_fig_old():

    df.sort_values('norm_eigen2ndsmallest', ascending=False, inplace=True)
    ax = df.plot(kind='bar', 
                x='Graph name', 
                y=['norm_eigen2ndsmallest','dist_to_bipartiteness'], 
                color=['red','steelblue'],
                title='Second smallest eigenvalue and distance to bipartiteness of each network',
                ylabel='Normalised Value',
                fontsize=12)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
    ax.legend(['$\lambda_2$', '$2-\lambda_n$'])
    ax.title.set_fontsize(14)
    ax.xaxis.label.set_fontsize(12)
    ax.yaxis.label.set_fontsize(12)
    plt.tight_layout()
    plt.show()




