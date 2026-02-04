# src/utils/visualization.py

import matplotlib.pyplot as plt
import networkx as nx

def draw_graph(graph, traversal_order=None, title="", save_path=None):
    G = nx.DiGraph() if graph.directed else nx.Graph()
    for u in graph.nodes:
        for v, w in graph.get_neighbors(u):
            G.add_edge(u, v, weight=w)

    pos = nx.spring_layout(G, seed=42)
    plt.figure(figsize=(8, 6))
    nx.draw(G, pos, with_labels=True, node_color='lightblue', edge_color='gray', node_size=500)

    if traversal_order:
        nx.draw_networkx_nodes(G, pos, nodelist=traversal_order, node_color='orange')

    plt.title(title)
    if save_path:
        plt.savefig(save_path)
    plt.close()
