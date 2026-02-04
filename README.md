# Week 4 Graph Algorithms Project

## Project Overview
This project implements and benchmarks graph algorithms including:

- Graph representation (adjacency list & adjacency matrix)
- Breadth-First Search (BFS)
- Depth-First Search (DFS, iterative & recursive)
- Dijkstra's shortest path algorithm
- Benchmarking and visualization of performance

The project demonstrates the impact of graph structure (sparse vs dense, weighted vs unweighted) on traversal and shortest path performance.

https://github.com/Throwbias/Algorithms_Course.git
---

## Project Structure
week4_project/
├── README.md
├── src/
│ ├── graphs/
│ │ ├── graph.py
│ │ ├── bfs.py
│ │ ├── dfs.py
│ │ ├── dijkstra.py
│ │ └── init.py
│ └── utils/
│ ├── graph_generator.py
│ └── visualization.py
├── benchmarks/
│ ├── week4_graph_benchmark.py
│ └── results/
│ ├── bfs_sparse_.png
│ ├── bfs_dense_.png
│ ├── dfs_sparse_.png
│ ├── dfs_dense_.png
│ ├── dijkstra_*.png
│ └── comparison_table.csv
├── tests/
│ ├── test_graph_representation.py
│ ├── test_bfs.py
│ ├── test_dfs.py
│ ├── test_dijkstra.py
│ └── test_graph_benchmark.py
└── analysis/
└── week4_report.md


---

## Setup

1. **Create and activate virtual environment**:

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate
Install dependencies:

pip install -r requirements.txt
Running Benchmarks
Generate performance benchmarks and traversal visualizations:

python -m benchmarks.week4_graph_benchmark
Outputs will be saved in benchmarks/results/:

BFS and DFS traversal visualizations: bfs_sparse_*.png, dfs_dense_*.png

Dijkstra performance plots: dijkstra_*.png

Comparison table: comparison_table.csv

Running Tests
Run all unit tests for graph, traversal, and shortest path algorithms:

pytest -v tests/
All core algorithms are tested:

Graph representation (add nodes, add edges, adjacency list & matrix)

BFS and DFS correctness

Dijkstra shortest path

Benchmarking utilities

Notes
Graphs can be directed or undirected, weighted or unweighted.

Benchmarks compare sparse vs dense graphs and list vs matrix representations.

Visualizations use NetworkX and Matplotlib.

Designed for clarity and modularity to easily extend or modify algorithms.

References
NetworkX: https://networkx.org/

Matplotlib: https://matplotlib.org/

Python heapq for priority queues in Dijkstra's algorithm