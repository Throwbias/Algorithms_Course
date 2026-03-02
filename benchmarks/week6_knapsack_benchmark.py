"""
Week 6 Knapsack Benchmark
Compares Week 5 bottom-up DP (knapsack_tabulated) vs Week 6 space-optimized DP
Measures runtime and peak memory usage and generates a comparison plot.
"""

import sys
import os
import time
import tracemalloc
import matplotlib.pyplot as plt

# Add src folder to Python path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

# ---------- Imports ----------
from dp.knapsack import knapsack_tabulated  # Week 5 bottom-up DP
from dp_advanced.space_optimized_knapsack import knapsack_space_optimized  # Week 6

# ---------- Test Data ----------
N = 150  # number of items
weights = [i for i in range(1, N+1)]
values = [i*2 for i in range(1, N+1)]
capacity = 150

# ---------- Benchmark Function ----------
def benchmark(func, weights, values, capacity):
    tracemalloc.start()
    start_time = time.perf_counter()
    # knapsack_tabulated returns (value, table)
    if func == knapsack_tabulated:
        result, _ = func(weights, values, capacity)
    else:
        result = func(weights, values, capacity)
    end_time = time.perf_counter()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return {
        "name": func.__name__,
        "result": result,
        "time": end_time - start_time,
        "peak_mem_kb": peak / 1024
    }

# ---------- Run Benchmarks ----------
results = []
for func in [knapsack_tabulated, knapsack_space_optimized]:
    res = benchmark(func, weights, values, capacity)
    results.append(res)
    print(f"{res['name']}: result={res['result']}, time={res['time']:.6f}s, peak_mem={res['peak_mem_kb']:.2f} KB")

# ---------- Plot Results ----------
names = [r['name'] for r in results]
mem = [r['peak_mem_kb'] for r in results]
time_vals = [r['time'] for r in results]

plt.figure(figsize=(10,5))

plt.subplot(1,2,1)
plt.bar(names, mem, color=['blue','green'])
plt.ylabel("Peak Memory (KB)")
plt.title("Memory Usage Comparison")

plt.subplot(1,2,2)
plt.bar(names, time_vals, color=['blue','green'])
plt.ylabel("Runtime (s)")
plt.title("Runtime Comparison")

plt.tight_layout()

# Ensure results folder exists
os.makedirs(os.path.join(os.path.dirname(__file__), 'results'), exist_ok=True)
plt.savefig(os.path.join(os.path.dirname(__file__), 'results', 'knapsack_comparison.png'))
plt.show()