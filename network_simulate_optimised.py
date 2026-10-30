"""
This is my original network4_simulate.py file but optimised to run faster because it was way too slow.
Optimised with the help of deepseek"""

import networkx as nx
import random
import pandas as pd
from pathlib import Path
from network_generate import files_sift, graph_weightify
import time
import os

NO_SEEDS = 1000000

def precompute_paths_and_mapping(G):
    """
    Returns:
        nodes: list of node names in the same order as G.nodes()
        node_to_idx: dict {node_name: index}
        paths: 2D list paths[i][j] = list of node indices (including both ends)
    """
    nodes = list(G.nodes())          # keep original order for random.sample
    n = len(nodes)
    node_to_idx = {node: i for i, node in enumerate(nodes)}

    # Precompute all-pairs shortest paths (by node names)
    all_paths = dict(nx.all_pairs_dijkstra_path(G, weight='weight'))

    # Convert to index-based paths for fast lookups
    paths = [[None] * n for _ in range(n)]
    for src_name, dst_dict in all_paths.items():
        i = node_to_idx[src_name]
        for dst_name, path_names in dst_dict.items():
            j = node_to_idx[dst_name]
            paths[i][j] = [node_to_idx[node] for node in path_names]
    return nodes, paths

def transmit_optimized(nodes, paths, seed, n_nodes):
    """Single seed using precomputed paths and bitmask channels."""
    random.seed(seed)
    channels = n_nodes * (n_nodes + 1) // 2
    full_mask = (1 << channels) - 1
    node_masks = [full_mask] * n_nodes   # each node's available channels as bits

    counter = 0
    while True:
        # Pick two distinct nodes from the original node list (preserving order)
        src_name, tgt_name = random.sample(nodes, 2)
        src_idx = node_to_idx[src_name]  # but we need node_to_idx here – we'll pass it
        tgt_idx = node_to_idx[tgt_name]
        path = paths[src_idx][tgt_idx]

        # Compute common free channels along the path
        common = node_masks[path[0]]
        for idx in path[1:]:
            common &= node_masks[idx]
            if common == 0:
                break

        if common == 0:
            break   # block
        else:
            # Get lowest set bit (same as first index where channel_mult == 1)
            ch_idx = (common & -common).bit_length() - 1
            bit = 1 << ch_idx
            for idx in path:
                node_masks[idx] &= ~bit
            counter += 1

    return counter

def many_seeds_tx_optimized(G, seeds):
    """Run many seeds with precomputed data."""
    nodes, paths = precompute_paths_and_mapping(G)
    n_nodes = len(nodes)
    # Build node_to_idx mapping again for use inside transmit_optimized
    global node_to_idx  # hack for simplicity; better to pass as argument
    node_to_idx = {node: i for i, node in enumerate(nodes)}
    
    results = []
    for seed in range(seeds):
        txs = transmit_optimized(nodes, paths, seed, n_nodes)
        results.append(txs)
    results.sort()
    return results

def run_save_simulation():
    suitable_files = files_sift()   # returns stage3_sift graphs

    for file in suitable_files[:2]:     # change to suitable_files[2:3] for single test
        print(f"\nProcessing {file} ...")
        G, topology = graph_weightify(file)
        n_nodes = G.number_of_nodes()
        channels = n_nodes * (n_nodes + 1) // 2

        start = time.time()
        txs_to_block = many_seeds_tx_optimized(G, NO_SEEDS)
        elapsed = time.time() - start
        print(f"  Completed {NO_SEEDS} seeds in {elapsed:.1f} seconds")

        # Empirical CDF: x/(N+1)
        probs = [(i + 1) / (NO_SEEDS + 1) for i in range(NO_SEEDS)]

        os.chdir(Path.cwd().parent)
        current_dir = Path.cwd()
        data_folder = current_dir / "net4csv_files"
        data_folder.mkdir(parents=True, exist_ok=True)

        list_of_tuples = list(zip(probs, txs_to_block))

        # Converting lists of tuples into pandas Dataframe.
        df = pd.DataFrame(list_of_tuples, columns=['Probability', 'Txs until block'])

        # set up file name with relevant simulation parameters
        filename = f'top-{topology}-ch-{channels}-seeds-{NO_SEEDS}-.csv'
        full_path = data_folder / filename

        df.to_csv(full_path, index=False)

        current_dir = Path.cwd()

        graph_folder = current_dir / "TopologyZooGraphs"
        graph_folder.mkdir(parents=True, exist_ok=True)
        os.chdir(graph_folder)

        current_dir = Path.cwd()


if __name__ == "__main__":
    run_save_simulation()