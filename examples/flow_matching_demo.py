import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.flow.applications.matching import bipartite_matching


left = ["Alice", "Bob", "Cara"]
right = ["Task1", "Task2", "Task3"]

edges = [
    ("Alice", "Task1"),
    ("Alice", "Task2"),
    ("Bob", "Task2"),
    ("Cara", "Task1"),
    ("Cara", "Task3"),
]

result = bipartite_matching(left, right, edges, solver="ek")

print("Matching size:", result["matching_size"])
print("Matching pairs:")
for pair in result["matching_pairs"]:
    print(pair)