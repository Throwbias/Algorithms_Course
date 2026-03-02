"""
Week 6 DP Advanced Benchmark
Benchmarks:
- Standard (2D) vs Space-Optimized Knapsack
- MCM Recursive (memoized) vs MCM Bottom-up DP
- Floyd–Warshall scaling (n = 50, 100, 200, 500)
- TSP Bitmask DP vs Brute Force (up to 12 cities)
Exports:
- benchmarks/results/knapsack_space_comparison.png
- benchmarks/results/mcm_performance.png
- benchmarks/results/floyd_warshall_scaling.png
- benchmarks/results/tsp_bitmask_runtime.png
- benchmarks/results/comparison_table.csv
"""

import os
import sys
import time
import math
import random
import itertools
import tracemalloc
import csv

import matplotlib.pyplot as plt

# Ensure imports from src/
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

# ---------- Imports (your implementations) ----------
from dp.knapsack import knapsack_tabulated
from dp_advanced.space_optimized_knapsack import knapsack_space_optimized

from dp_advanced.matrix_chain_multiplication import mcm_recursive, mcm_tabulated
from dp_advanced.floyd_warshall import floyd_warshall
from dp_advanced.bitmask_traveling_salesman import tsp_bitmask  


RESULTS_DIR = os.path.join(os.path.dirname(__file__), "results")


# ---------- Helpers ----------
def ensure_results_dir():
    os.makedirs(RESULTS_DIR, exist_ok=True)


def benchmark_time_and_peak_mem(func, *args, repeats=3, warmup=1, **kwargs):
    """
    Returns dict with:
      time_sec: best runtime across repeats (after warmup)
      peak_mem_kb: peak tracemalloc memory during best run
      result: result from best run (optional use)
    """
    # warmup runs (no tracemalloc)
    for _ in range(warmup):
        func(*args, **kwargs)

    best_time = float("inf")
    best_peak_kb = None
    best_result = None

    for _ in range(repeats):
        tracemalloc.start()
        t0 = time.perf_counter()
        result = func(*args, **kwargs)
        t1 = time.perf_counter()
        _, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        dt = t1 - t0
        if dt < best_time:
            best_time = dt
            best_peak_kb = peak / 1024
            best_result = result

    return {"time_sec": best_time, "peak_mem_kb": best_peak_kb, "result": best_result}


def save_csv(rows, filename, fieldnames):
    path = os.path.join(RESULTS_DIR, filename)
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    return path


def gen_random_dims(n, low=5, high=50, seed=42):
    rng = random.Random(seed)
    # dims length n+1
    return [rng.randint(low, high) for _ in range(n + 1)]


def gen_dense_weighted_graph(n, density=0.35, wmin=-5, wmax=20, seed=42):
    """
    Floyd–Warshall expects adjacency matrix with math.inf for no edge.
    No negative cycles guaranteed (we avoid creating guaranteed cycles; still could happen in theory with negatives).
    For sanity, keep negatives sparse-ish and include zero diagonal.
    """
    rng = random.Random(seed + n)
    inf = math.inf
    g = [[inf] * n for _ in range(n)]
    for i in range(n):
        g[i][i] = 0

    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            if rng.random() < density:
                w = rng.randint(wmin, wmax)
                g[i][j] = w
    return g


def gen_metric_tsp(n, seed=42):
    """
    Generate Euclidean points and use distances => symmetric metric TSP.
    """
    rng = random.Random(seed + n)
    pts = [(rng.random(), rng.random()) for _ in range(n)]
    dist = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i == j:
                dist[i][j] = 0.0
            else:
                dx = pts[i][0] - pts[j][0]
                dy = pts[i][1] - pts[j][1]
                dist[i][j] = (dx * dx + dy * dy) ** 0.5
    return dist


def tsp_bruteforce(dist):
    """
    Brute force TSP for n up to ~10-12 max (factorial blows up).
    Returns (best_cost, best_tour)
    """
    n = len(dist)
    best = float("inf")
    best_tour = None
    for perm in itertools.permutations(range(1, n)):
        tour = (0,) + perm + (0,)
        cost = 0.0
        ok = True
        for i in range(n):
            c = dist[tour[i]][tour[i + 1]]
            if c == float("inf"):
                ok = False
                break
            cost += c
        if ok and cost < best:
            best = cost
            best_tour = list(tour)
    return best, best_tour


# ---------- Benchmarks ----------
def run_knapsack():
    # Same style as your existing knapsack benchmark, but produces required filename
    N = 200
    weights = list(range(1, N + 1))
    values = [i * 2 for i in range(1, N + 1)]
    capacity = 250

    def run_tab():
        v, _ = knapsack_tabulated(weights, values, capacity)
        return v

    def run_opt():
        return knapsack_space_optimized(weights, values, capacity)

    r_tab = benchmark_time_and_peak_mem(run_tab, repeats=5, warmup=1)
    r_opt = benchmark_time_and_peak_mem(run_opt, repeats=5, warmup=1)

    # plot
    names = ["knapsack_tabulated_2d", "knapsack_space_optimized_1d"]
    mem = [r_tab["peak_mem_kb"], r_opt["peak_mem_kb"]]
    times = [r_tab["time_sec"], r_opt["time_sec"]]

    plt.figure(figsize=(10, 5))
    plt.subplot(1, 2, 1)
    plt.bar(names, mem)
    plt.ylabel("Peak Memory (KB)")
    plt.title("Knapsack Peak Memory")

    plt.subplot(1, 2, 2)
    plt.bar(names, times)
    plt.ylabel("Runtime (s)")
    plt.title("Knapsack Runtime")

    plt.tight_layout()
    out = os.path.join(RESULTS_DIR, "knapsack_space_comparison.png")
    plt.savefig(out)
    plt.close()

    return {
        "standard_time": r_tab["time_sec"],
        "standard_mem_kb": r_tab["peak_mem_kb"],
        "opt_time": r_opt["time_sec"],
        "opt_mem_kb": r_opt["peak_mem_kb"],
        "plot": out,
    }


def run_mcm():
    # Compare recursive memo vs bottom-up
    sizes = [10, 20, 30, 40, 60]  # n matrices (dims length n+1)
    rec_times = []
    dp_times = []

    for n in sizes:
        p = gen_random_dims(n, low=5, high=60, seed=99)

        # recursive memoized
        def rec():
            memo = {}
            split = {}
            return mcm_recursive(p, memo=memo, split=split)

        # bottom-up
        def tab():
            return mcm_tabulated(p)[0]

        r1 = benchmark_time_and_peak_mem(rec, repeats=3, warmup=1)
        r2 = benchmark_time_and_peak_mem(tab, repeats=3, warmup=1)

        rec_times.append(r1["time_sec"])
        dp_times.append(r2["time_sec"])

    plt.figure(figsize=(8, 5))
    plt.plot(sizes, rec_times, marker="o", label="MCM Recursive (memo)")
    plt.plot(sizes, dp_times, marker="o", label="MCM Bottom-up DP")
    plt.xlabel("Number of Matrices (n)")
    plt.ylabel("Runtime (s)")
    plt.title("MCM Runtime: Recursive vs DP")
    plt.legend()
    out = os.path.join(RESULTS_DIR, "mcm_performance.png")
    plt.savefig(out)
    plt.close()

    return {"sizes": sizes, "rec_times": rec_times, "dp_times": dp_times, "plot": out}


def run_floyd_warshall():
    # Required sizes in prompt
    sizes = [50, 100, 200, 500]
    times = []
    mems = []

    for n in sizes:
        g = gen_dense_weighted_graph(n, density=0.25, wmin=1, wmax=25, seed=7)  # keep positive to avoid neg cycles

        def fw():
            dist, nxt = floyd_warshall(g)
            return dist[0][0]  # force compute usage

        r = benchmark_time_and_peak_mem(fw, repeats=2, warmup=1)
        times.append(r["time_sec"])
        mems.append(r["peak_mem_kb"])

    plt.figure(figsize=(8, 5))
    plt.plot(sizes, times, marker="o")
    plt.xlabel("Number of Vertices (V)")
    plt.ylabel("Runtime (s)")
    plt.title("Floyd–Warshall Scaling (Runtime)")
    out = os.path.join(RESULTS_DIR, "floyd_warshall_scaling.png")
    plt.savefig(out)
    plt.close()

    return {"sizes": sizes, "times": times, "mems": mems, "plot": out}


def run_tsp():
    # Compare bitmask vs brute-force up to 12 (brute force gets ugly fast)
    sizes = [6, 7, 8, 9, 10, 11, 12]
    bitmask_times = []
    brute_times = []

    for n in sizes:
        dist = gen_metric_tsp(n, seed=123)

        def bm():
            return tsp_bitmask(dist)[0]

        rbm = benchmark_time_and_peak_mem(bm, repeats=3, warmup=1)
        bitmask_times.append(rbm["time_sec"])

        # brute-force: fewer repeats
        def bf():
            return tsp_bruteforce(dist)[0]

        rbf = benchmark_time_and_peak_mem(bf, repeats=1, warmup=0)
        brute_times.append(rbf["time_sec"])

    plt.figure(figsize=(8, 5))
    plt.plot(sizes, bitmask_times, marker="o", label="Bitmask DP (Held–Karp)")
    plt.plot(sizes, brute_times, marker="o", label="Brute Force")
    plt.xlabel("Number of Cities (n)")
    plt.ylabel("Runtime (s)")
    plt.title("TSP Runtime: Bitmask DP vs Brute Force")
    plt.legend()
    out = os.path.join(RESULTS_DIR, "tsp_bitmask_runtime.png")
    plt.savefig(out)
    plt.close()

    return {"sizes": sizes, "bitmask_times": bitmask_times, "brute_times": brute_times, "plot": out}


def main():
    ensure_results_dir()

    print("Running Week 6 DP Advanced Benchmarks...\n")

    kn = run_knapsack()
    print(f"[OK] Knapsack plot: {kn['plot']}")

    mcm = run_mcm()
    print(f"[OK] MCM plot: {mcm['plot']}")

    fw = run_floyd_warshall()
    print(f"[OK] Floyd–Warshall plot: {fw['plot']}")

    tsp = run_tsp()
    print(f"[OK] TSP plot: {tsp['plot']}")

    # Build one comparison CSV (summary)
    rows = []

    rows.append({
        "experiment": "knapsack_standard_2d",
        "n_or_v": "N=200,W=250",
        "time_sec": kn["standard_time"],
        "peak_mem_kb": kn["standard_mem_kb"],
        "notes": "Week 5 tabulation dp[n][W]"
    })
    rows.append({
        "experiment": "knapsack_space_optimized_1d",
        "n_or_v": "N=200,W=250",
        "time_sec": kn["opt_time"],
        "peak_mem_kb": kn["opt_mem_kb"],
        "notes": "Week 6 compressed dp[W]"
    })

    # MCM summary (last size as representative)
    rows.append({
        "experiment": "mcm_recursive_memo",
        "n_or_v": f"n={mcm['sizes'][-1]}",
        "time_sec": mcm["rec_times"][-1],
        "peak_mem_kb": "",
        "notes": "Top-down recursion + memo"
    })
    rows.append({
        "experiment": "mcm_bottom_up",
        "n_or_v": f"n={mcm['sizes'][-1]}",
        "time_sec": mcm["dp_times"][-1],
        "peak_mem_kb": "",
        "notes": "O(n^3) DP tabulation"
    })

    # Floyd summary (largest)
    rows.append({
        "experiment": "floyd_warshall",
        "n_or_v": f"V={fw['sizes'][-1]}",
        "time_sec": fw["times"][-1],
        "peak_mem_kb": fw["mems"][-1],
        "notes": "All-pairs shortest paths"
    })

    # TSP summary (largest)
    rows.append({
        "experiment": "tsp_bitmask_dp",
        "n_or_v": f"n={tsp['sizes'][-1]}",
        "time_sec": tsp["bitmask_times"][-1],
        "peak_mem_kb": "",
        "notes": "Held–Karp O(n^2*2^n)"
    })
    rows.append({
        "experiment": "tsp_bruteforce",
        "n_or_v": f"n={tsp['sizes'][-1]}",
        "time_sec": tsp["brute_times"][-1],
        "peak_mem_kb": "",
        "notes": "Brute force O(n!)"
    })

    csv_path = save_csv(
        rows,
        "comparison_table.csv",
        fieldnames=["experiment", "n_or_v", "time_sec", "peak_mem_kb", "notes"]
    )
    print(f"\n[OK] CSV summary: {csv_path}")
    print("\nDone.")


if __name__ == "__main__":
    main()