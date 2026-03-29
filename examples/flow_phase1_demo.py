import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.flow.network import FlowNetwork
from src.flow.edmonds_karp import edmonds_karp


network = FlowNetwork(4)
network.add_edge(0, 1, 3)
network.add_edge(0, 2, 2)
network.add_edge(1, 2, 1)
network.add_edge(1, 3, 2)
network.add_edge(2, 3, 4)

result = edmonds_karp(network, 0, 3)

print("Max flow:", result["max_flow"])
print("Iterations:", result["iterations"])
print("Bottlenecks:", result["bottlenecks"])
print("Paths:", result["augmenting_paths"])
print("Flow matrix:")
for row in result["flow_matrix"]:
    print(row)