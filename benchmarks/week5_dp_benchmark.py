"""
week5_dp_benchmark.py

Benchmarking script for Week 5 Dynamic Programming assignments:
Fibonacci, 0/1 Knapsack, and Longest Common Subsequence (LCS).

Generates CSV files and line plots comparing naive, memoized, and tabulated implementations.
"""

import time
import csv
import os
import matplotlib.pyplot as plt
from src.dp import fibonacci, knapsack, lcs
from src.utils.visualization import ensure_results_dir

# -----------------------------
# Benchmarking Helper
# -----------------------------
def benchmark_algorithm(funcs, input_sizes):
    """
    Benchmark a set of functions over multiple input sizes.
    
    funcs: dict of {name: function}
    input_sizes: list of integers
    Returns: list of result dictionaries
    """
    results = []

    for n in input_sizes:
        res = {"n": n}

        for name, func in funcs.items():
            # Determine if this function supports counter
            supports_counter = name.endswith("naive") or name.endswith("memo")

            counter = {"calls": 0} if supports_counter else None
            start = time.perf_counter()

            # Generate appropriate inputs based on problem type
            if name.startswith("fib"):
                if supports_counter:
                    func(n, counter=counter)
                else:
                    func(n)

            elif name.startswith("knap"):
                weights = list(range(1, n + 1))
                values = [w * 2 for w in weights]
                capacity = n * 2
                if supports_counter:
                    func(weights, values, capacity, counter=counter)
                else:
                    func(weights, values, capacity)

            elif name.startswith("lcs"):
                X = "A" * n
                Y = "A" * n
                if supports_counter:
                    func(X, Y, counter=counter)
                else:
                    func(X, Y)

            elapsed = time.perf_counter() - start
            res[f"{name}_time"] = elapsed
            res[f"{name}_calls"] = counter["calls"] if counter else None

        results.append(res)

    return results

# -----------------------------
# CSV Helper
# -----------------------------
def save_results_csv(results, filename):
    ensure_results_dir()
    keys = results[0].keys()
    with open(filename, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(results)
    print(f"Saved CSV: {filename}")

# -----------------------------
# Plotting Helpers
# -----------------------------
def plot_results(results, problem_name, y_label="Time (s)", filename=None):
    ensure_results_dir()
    ns = [r["n"] for r in results]

    plt.figure(figsize=(8,5))
    for key in results[0].keys():
        if key.endswith("_time") and key != "n":
            label = key.replace("_time","")
            plt.plot(ns, [r[key] for r in results], marker='o', label=label)

    plt.xlabel("Input size (n)")
    plt.ylabel(y_label)
    plt.title(f"{problem_name} Performance")
    plt.yscale("log")
    plt.grid(True, which="both", linestyle="--", linewidth=0.5)
    plt.legend()
    if filename is None:
        filename = f"benchmarks/results/{problem_name.lower().replace(' ','_')}_performance.png"
    plt.savefig(filename)
    plt.close()
    print(f"Saved plot: {filename}")

# -----------------------------
# Run Benchmarks
# -----------------------------
def run_benchmarks():
    # ---------------- Fibonacci ----------------
    print("Benchmarking Fibonacci...")
    fib_funcs = {
        "fib_naive": fibonacci.fib_recursive,
        "fib_memo": fibonacci.fib_memoized,
        "fib_tab": fibonacci.fib_tabulated
    }
    fib_ns = [10, 20, 30, 35]  # smaller sizes for naive recursive
    fib_results = benchmark_algorithm(fib_funcs, fib_ns)
    save_results_csv(fib_results, "benchmarks/results/dp_vs_recursive_fibonacci.csv")
    plot_results(fib_results, "Fibonacci")

    # ---------------- Knapsack ----------------
    print("Benchmarking 0/1 Knapsack...")
    knap_funcs = {
    "knap_naive": knapsack.knapsack_recursive,  
    "knap_memo": knapsack.knapsack_memoized,     
    "knap_tab": knapsack.knapsack_tabulated     
    }
    knap_ns = [5, 10, 15, 20]  # small input for naive
    knap_results = benchmark_algorithm(knap_funcs, knap_ns)
    save_results_csv(knap_results, "benchmarks/results/dp_vs_recursive_knapsack.csv")
    plot_results(knap_results, "Knapsack")

    # ---------------- LCS ----------------
    print("Benchmarking Longest Common Subsequence (LCS)...")
    lcs_funcs = {
        "lcs_naive": lcs.lcs_recursive,
        "lcs_memo": lcs.lcs_memoized,
        "lcs_tab": lcs.lcs_tabulated
    }
    lcs_ns = [5, 10, 20, 50]  # small for naive
    lcs_results = benchmark_algorithm(lcs_funcs, lcs_ns)
    save_results_csv(lcs_results, "benchmarks/results/dp_vs_recursive_lcs.csv")
    plot_results(lcs_results, "LCS")

    print("All benchmarks completed.")

# -----------------------------
# Script Entry
# -----------------------------
if __name__ == "__main__":
    run_benchmarks()
