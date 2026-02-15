"""
visualization.py

Reusable visualization utilities for benchmarking DP algorithms.

Features:
- Line plots for execution time, recursion calls, speedup
- Log scale support for time or input size
- Save figures automatically to results folder
"""

import os
import matplotlib.pyplot as plt
def ensure_results_dir():
    """
    Ensure the benchmarks/results directory exists.
    """
    results_dir = os.path.join("benchmarks", "results")
    os.makedirs(results_dir, exist_ok=True)
RESULTS_DIR = os.path.join(os.path.dirname(__file__), "../../benchmarks/results")
os.makedirs(RESULTS_DIR, exist_ok=True)


# -----------------------------
# Time vs Input Size Plot
# -----------------------------
def plot_time(results, algo_names, xlabel="Input Size", ylabel="Time (s)", title="Execution Time Comparison", log_scale=True, filename="time_plot.png"):
    """
    Plots execution time for multiple algorithms.

    results: list of lists, each containing times for corresponding algo
    algo_names: list of algorithm labels
    """
    plt.figure(figsize=(8, 6))

    n_values = [r["n"] for r in results]  # assumes all algos have same n-values

    for idx, name in enumerate(algo_names):
        times = [r[f"{name}_time"] for r in results]
        plt.plot(n_values, times, marker="o", label=name)

    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.legend()
    plt.grid(True)
    if log_scale:
        plt.yscale("log")
    plt.tight_layout()
    path = os.path.join(RESULTS_DIR, filename)
    plt.savefig(path)
    plt.close()
    print(f"Saved plot: {path}")


# -----------------------------
# Calls vs Input Size Plot
# -----------------------------
def plot_calls(results, algo_names, xlabel="Input Size", ylabel="Recursive Calls", title="Recursive Calls Comparison", log_scale=True, filename="calls_plot.png"):
    """
    Plots number of recursive calls for multiple algorithms.
    """
    plt.figure(figsize=(8, 6))

    n_values = [r["n"] for r in results]  # assumes all algos have same n-values

    for idx, name in enumerate(algo_names):
        calls = [r[f"{name}_calls"] for r in results]
        plt.plot(n_values, calls, marker="o", label=name)

    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.legend()
    plt.grid(True)
    if log_scale:
        plt.yscale("log")
    plt.tight_layout()
    path = os.path.join(RESULTS_DIR, filename)
    plt.savefig(path)
    plt.close()
    print(f"Saved plot: {path}")


# -----------------------------
# Speedup Factor Plot
# -----------------------------
def plot_speedup(results, baseline_name, compare_names, xlabel="Input Size", ylabel="Speedup (x)", title="Speedup over Baseline", filename="speedup_plot.png"):
    """
    Plots speedup factor of algorithms over a baseline.

    baseline_name: key for baseline algorithm (e.g., 'naive')
    compare_names: list of keys for algorithms to compare against baseline
    """
    plt.figure(figsize=(8, 6))

    n_values = [r["n"] for r in results]

    baseline_times = [r[f"{baseline_name}_time"] for r in results]

    for name in compare_names:
        comp_times = [r[f"{name}_time"] for r in results]
        speedup = [b / c for b, c in zip(baseline_times, comp_times)]
        plt.plot(n_values, speedup, marker="o", label=name)

    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    path = os.path.join(RESULTS_DIR, filename)
    plt.savefig(path)
    plt.close()
    print(f"Saved plot: {path}")
