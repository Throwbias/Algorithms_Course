import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.flow.network import FlowNetwork
from src.flow.push_relabel import push_relabel


network = FlowNetwork(4)
network.add_edge(0, 1, 3)
network.add_edge(0, 2, 2)
network.add_edge(1, 2, 1)
network.add_edge(1, 3, 2)
network.add_edge(2, 3, 4)

result = push_relabel(network, 0, 3)

print("Max flow:", result["max_flow"])
print("Push count:", result["push_count"])
print("Relabel count:", result["relabel_count"])
print("Discharge count:", result["discharge_count"])
print("Heights:", result["heights"])
print("Flow matrix:")
for row in result["flow_matrix"]:
    print(row)