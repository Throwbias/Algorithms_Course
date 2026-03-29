"""
Week 10 / Flow Network Benchmark

Benchmarks Edmonds-Karp vs Push-Relabel on random flow networks.

Outputs:
- benchmarks/results/flow_benchmark_results.csv
- benchmarks/results/flow_runtime_comparison.png
- benchmarks/results/flow_algorithm_counts.png
"""

import os
import sys
import time
import random
import pandas as pd
import matplotlib.pyplot as plt

# Ensure project root is importable
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.flow.network import FlowNetwork
from src.flow.edmonds_karp import edmonds_karp
from src.flow.push_relabel import push_relabel


RESULTS_DIR = os.path.join("benchmarks", "results")
CSV_PATH = os.path.join(RESULTS_DIR, "flow_benchmark_results.csv")


def ensure_output_dir(path):
    os.makedirs(path, exist_ok=True)


def generate_random_flow_network(num_vertices, edge_probability=0.15, seed=42, capacity_range=(1, 20)):
    """
    Generate a random directed flow network with source=0 and sink=n-1.
    Adds some guaranteed forward connectivity so source/sink are not isolated.
    """
    rng = random.Random(seed)
    network = FlowNetwork(num_vertices)

    # Backbone path to help guarantee connectivity from source to sink
    for i in range(num_vertices - 1):
        network.add_edge(i, i + 1, rng.randint(*capacity_range))

    # Additional random forward edges
    for u in range(num_vertices):
        for v in range(num_vertices):
            if u == v:
                continue
            if v <= u:
                continue  # keep it mostly forward to reduce weird degenerate graphs
            if rng.random() < edge_probability:
                network.add_edge(u, v, rng.randint(*capacity_range))

    return network


def clone_network(network):
    """
    Deep-copy a FlowNetwork by recreating only original edges.
    """
    cloned = FlowNetwork(network.num_vertices)
    for u in range(network.num_vertices):
        for edge in network.graph[u]:
            if not edge.is_reverse and edge.original_capacity > 0:
                cloned.add_edge(u, edge.to, edge.original_capacity)
    return cloned


def benchmark_edmonds_karp(network, source, sink):
    test_network = clone_network(network)
    start = time.perf_counter()
    result = edmonds_karp(test_network, source, sink)
    runtime = time.perf_counter() - start

    return {
        "algorithm": "Edmonds-Karp",
        "runtime_sec": runtime,
        "max_flow": result["max_flow"],
        "iterations": result["iterations"],
        "aux_count": result["residual_updates"],
    }


def benchmark_push_relabel(network, source, sink):
    test_network = clone_network(network)
    start = time.perf_counter()
    result = push_relabel(test_network, source, sink)
    runtime = time.perf_counter() - start

    return {
        "algorithm": "Push-Relabel",
        "runtime_sec": runtime,
        "max_flow": result["max_flow"],
        "iterations": result["discharge_count"],
        "aux_count": result["push_count"] + result["relabel_count"],
    }


def run_benchmarks():
    ensure_output_dir(RESULTS_DIR)

    rows = []

    # Keep sizes moderate first so it runs reliably on Windows
    sizes = [20, 40, 60, 80, 100, 150, 200]
    densities = [0.10, 0.20]

    for density in densities:
        for n in sizes:
            seed = 1000 + n + int(density * 100)
            base_network = generate_random_flow_network(
                num_vertices=n,
                edge_probability=density,
                seed=seed,
                capacity_range=(1, 25),
            )

            source = 0
            sink = n - 1

            ek_row = benchmark_edmonds_karp(base_network, source, sink)
            ek_row["input_size"] = n
            ek_row["density"] = density
            rows.append(ek_row)

            pr_row = benchmark_push_relabel(base_network, source, sink)
            pr_row["input_size"] = n
            pr_row["density"] = density
            rows.append(pr_row)

            print(
                f"Completed n={n}, density={density:.2f} | "
                f"EK={ek_row['runtime_sec']:.6f}s, PR={pr_row['runtime_sec']:.6f}s"
            )

    df = pd.DataFrame(rows)
    df.to_csv(CSV_PATH, index=False)

    save_runtime_plot(df)
    save_counts_plot(df)

    print(f"\nSaved CSV: {CSV_PATH}")
    print(f"Saved plot: {os.path.join(RESULTS_DIR, 'flow_runtime_comparison.png')}")
    print(f"Saved plot: {os.path.join(RESULTS_DIR, 'flow_algorithm_counts.png')}")
    print("\nBenchmark preview:")
    print(df.head())


def save_runtime_plot(df):
    plt.figure(figsize=(10, 6))

    for algorithm in df["algorithm"].unique():
        subset = df[df["algorithm"] == algorithm]
        grouped = subset.groupby("input_size", as_index=False)["runtime_sec"].mean()
        plt.plot(grouped["input_size"], grouped["runtime_sec"], marker="o", label=algorithm)

    plt.xlabel("Number of Vertices")
    plt.ylabel("Runtime (seconds)")
    plt.title("Flow Algorithm Runtime Comparison")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(RESULTS_DIR, "flow_runtime_comparison.png"))
    plt.close()


def save_counts_plot(df):
    plt.figure(figsize=(10, 6))

    for algorithm in df["algorithm"].unique():
        subset = df[df["algorithm"] == algorithm]
        grouped = subset.groupby("input_size", as_index=False)["iterations"].mean()
        plt.plot(grouped["input_size"], grouped["iterations"], marker="o", label=algorithm)

    plt.xlabel("Number of Vertices")
    plt.ylabel("Average Iteration / Work Count")
    plt.title("Flow Algorithm Work Comparison")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(RESULTS_DIR, "flow_algorithm_counts.png"))
    plt.close()


if __name__ == "__main__":
    run_benchmarks()