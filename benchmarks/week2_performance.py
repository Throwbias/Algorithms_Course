import sys
import os

# --- Ensure project root is in Python path ---
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# --- Standard imports ---
import random
import csv
import time
import matplotlib.pyplot as plt

# --- Algorithm imports ---
from src.sorting.basic_sorts import bubble_sort, selection_sort, insertion_sort
from src.sorting.merge_sort import merge_sort
from src.sorting.quick_sort import quick_sort

# --- Configuration ---
ALGORITHMS = {
    "bubble_sort": bubble_sort,
    "selection_sort": selection_sort,
    "insertion_sort": insertion_sort,
    "merge_sort": merge_sort,
    "quick_sort": quick_sort
}

INPUT_SIZES = [100, 500, 1000, 5000, 10000, 50000]

DATA_TYPES = {
    "random": lambda n: [random.randint(0, n) for _ in range(n)],
    "sorted": lambda n: list(range(n)),
    "reverse_sorted": lambda n: list(range(n, 0, -1)),
    "nearly_sorted": lambda n: list(range(n-1)) + [0],
    "many_duplicates": lambda n: [random.randint(0, 9) for _ in range(n)],
    "few_unique": lambda n: [random.choice([0,1,2]) for _ in range(n)]
}

RESULTS_DIR = "benchmarks/results"
os.makedirs(RESULTS_DIR, exist_ok=True)
CSV_FILE = os.path.join(RESULTS_DIR, "week2_comparison.csv")

# --- Benchmark function ---
def benchmark_algorithm(func, data):
    """Time a single run of func on data"""
    start = time.perf_counter()
    func(list(data))  # use a copy to avoid modifying input
    end = time.perf_counter()
    return end - start

# --- Run benchmarks ---
results = []

for data_name, generator in DATA_TYPES.items():
    for size in INPUT_SIZES:
        data = generator(size)
        row = {"data_type": data_name, "size": size}
        for name, func in ALGORITHMS.items():
            # Repeat 3 times and take average
            times = [benchmark_algorithm(func, data) for _ in range(3)]
            row[name] = sum(times) / len(times)
        results.append(row)
        print(f"Completed {data_name} size {size}")

# --- Save results to CSV ---
with open(CSV_FILE, "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["data_type", "size"] + list(ALGORITHMS.keys()))
    writer.writeheader()
    writer.writerows(results)

print(f"\nBenchmark results saved to {CSV_FILE}")

# --- Generate plots ---
for data_name in DATA_TYPES.keys():
    plt.figure()
    for alg in ALGORITHMS.keys():
        times = [r[alg] for r in results if r["data_type"] == data_name]
        plt.plot(INPUT_SIZES, times, label=alg)
    plt.xlabel("Input Size")
    plt.ylabel("Time (seconds)")
    plt.title(f"{data_name.replace('_', ' ').title()} Data Benchmark")
    plt.legend()
    plot_file = os.path.join(RESULTS_DIR, f"{data_name}_plot.png")
    plt.savefig(plot_file)
    plt.close()
    print(f"Plot saved: {plot_file}")
