# Week 4 Graph Algorithms Project

## Project Overview
This project implements and benchmarks fundamental graph algorithms, including:

- Graph representations (adjacency list and adjacency matrix)
- Breadth-First Search (BFS)
- Depth-First Search (DFS – iterative and recursive)
- Dijkstra’s shortest path algorithm
- Performance benchmarking and visualization

The project explores how graph structure (sparse vs. dense, weighted vs. unweighted) and representation affect traversal and shortest-path performance.

**Repository:**  
https://github.com/Throwbias/Algorithms_Course.git

---

## Project Structure
Algorithms_Course/
├── README.md  
├── src/  
│   ├── graphs/  
│   │   ├── graph.py  
│   │   ├── bfs.py  
│   │   ├── dfs.py  
│   │   ├── dijkstra.py  
│   │   └── __init__.py  
│   └── utils/  
│       ├── graph_generator.py  
│       └── visualization.py  
├── benchmarks/  
│   ├── week4_graph_benchmark.py  
│   └── results/  
│       ├── bfs_sparse_*.png  
│       ├── bfs_dense_*.png  
│       ├── dfs_sparse_*.png  
│       ├── dfs_dense_*.png  
│       ├── dijkstra_*.png  
│       └── comparison_table.csv  
├── tests/  
│   ├── test_graph_representation.py  
│   ├── test_bfs.py  
│   ├── test_dfs.py  
│   ├── test_dijkstra.py  
│   └── test_graph_benchmark.py  
└── analysis/  
    └── week4_report.md  

---

## Setup

**Create and activate a virtual environment**

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

**Install Dependencies**

pip install -r requirements.txt

**Running Benchmarks**
Generate performance benchmarks and traversal visualizations:

python -m benchmarks.week4_graph_benchmark
Outputs will be saved in benchmarks/results/:

BFS and DFS traversal visualizations: bfs_sparse_*.png, dfs_dense_*.png

Dijkstra performance plots: dijkstra_*.png

Comparison table: comparison_table.csv

**Running Tests**
Run all unit tests for graph, traversal, and shortest path algorithms:

pytest -v tests/
All core algorithms are tested:

Graph representation (add nodes, add edges, adjacency list & matrix)

BFS and DFS correctness

Dijkstra shortest path

Benchmarking utilities

**Notes**
Graphs can be directed or undirected, weighted or unweighted.

Benchmarks compare sparse vs dense graphs and list vs matrix representations.

Visualizations use NetworkX and Matplotlib.

Designed for clarity and modularity to easily extend or modify algorithms.

**References**
NetworkX: https://networkx.org/

Matplotlib: https://matplotlib.org/

Python heapq for priority queues in Dijkstra's algorithm