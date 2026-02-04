# benchmarks/week4_graph_benchmark.py

import time
import csv
from pathlib import Path

from src.utils.graph_generator import generate_sparse_graph, generate_dense_graph
from src.utils.visualization import draw_graph
from src.graphs.bfs import bfs
from src.graphs.dfs import dfs_iterative  # Using iterative DFS
from src.graphs.dijkstra import dijkstra

RESULTS_DIR = Path(__file__).parent / "results"
RESULTS_DIR.mkdir(exist_ok=True)

# Graph sizes to benchmark
GRAPH_SIZES = [100, 500, 1000]  # you can adjust as needed

# Prepare CSV comparison table
comparison_table = RESULTS_DIR / "comparison_table.csv"

def benchmark_traversal(graph, algo, start_node=0):
    """Benchmark BFS or DFS traversal."""
    start = time.time()
    order = algo(graph, start_node)
    elapsed = time.time() - start
    return elapsed, order

def benchmark_dijkstra(graph, start_node=0):
    """Benchmark Dijkstra's algorithm."""
    start = time.time()
    distances, predecessors = dijkstra(graph, start_node)
    elapsed = time.time() - start
    return elapsed, distances, predecessors

def run_benchmarks():
    rows = [["Size",
             "BFS Sparse (s)", "DFS Sparse (s)", "Dijkstra Sparse (s)",
             "BFS Dense (s)", "DFS Dense (s)", "Dijkstra Dense (s)"]]

    for n in GRAPH_SIZES:
        print(f"\nBenchmarking graph size: {n}")

        # Generate graphs
        sparse = generate_sparse_graph(n)
        dense = generate_dense_graph(n)

        # ------------------------
        # BFS and DFS Sparse Graph
        # ------------------------
        t_bfs_sparse, bfs_order_sparse = benchmark_traversal(sparse, bfs)
        t_dfs_sparse, dfs_order_sparse = benchmark_traversal(sparse, dfs_iterative)
        t_dijkstra_sparse, _, _ = benchmark_dijkstra(sparse)

        # Save traversal plots
        draw_graph(sparse, bfs_order_sparse, f"BFS Sparse Graph ({n} nodes)",
                   RESULTS_DIR / f"bfs_sparse_{n}.png")
        draw_graph(sparse, dfs_order_sparse, f"DFS Sparse Graph ({n} nodes)",
                   RESULTS_DIR / f"dfs_sparse_{n}.png")

        # -----------------------
        # BFS and DFS Dense Graph
        # -----------------------
        t_bfs_dense, bfs_order_dense = benchmark_traversal(dense, bfs)
        t_dfs_dense, dfs_order_dense = benchmark_traversal(dense, dfs_iterative)
        t_dijkstra_dense, _, _ = benchmark_dijkstra(dense)

        # Save traversal plots
        draw_graph(dense, bfs_order_dense, f"BFS Dense Graph ({n} nodes)",
                   RESULTS_DIR / f"bfs_dense_{n}.png")
        draw_graph(dense, dfs_order_dense, f"DFS Dense Graph ({n} nodes)",
                   RESULTS_DIR / f"dfs_dense_{n}.png")

        # ------------------------
        # Append row to CSV table
        # ------------------------
        rows.append([
            n,
            t_bfs_sparse, t_dfs_sparse, t_dijkstra_sparse,
            t_bfs_dense, t_dfs_dense, t_dijkstra_dense
        ])

        # Print for console
        print(f"Sparse:  BFS={t_bfs_sparse:.6f}s, DFS={t_dfs_sparse:.6f}s, Dijkstra={t_dijkstra_sparse:.6f}s")
        print(f"Dense:   BFS={t_bfs_dense:.6f}s, DFS={t_dfs_dense:.6f}s, Dijkstra={t_dijkstra_dense:.6f}s")

    # Save CSV
    with open(comparison_table, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(rows)

    print(f"\nBenchmark complete! Results saved in {RESULTS_DIR}")

if __name__ == "__main__":
    run_benchmarks()
