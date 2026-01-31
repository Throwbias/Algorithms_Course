import time
import csv
import random
import matplotlib.pyplot as plt
from src.structures.heap import BinaryHeap
from src.structures.avl_tree import AVLTree
from src.structures.hash_table import HashTable

# -------------------- BENCHMARK SETTINGS --------------------
SIZES = [10**3, 10**4, 10**5]  # extendable to 10**6
NUM_TRIALS = 3
RESULTS_CSV = "benchmarks/results/week3_structures_results.csv"

# -------------------- HELPER FUNCTIONS --------------------
def benchmark_insert(structure, values):
    start = time.time()
    for v in values:
        if isinstance(structure, BinaryHeap):
            structure.insert(v)
        elif isinstance(structure, AVLTree):
            structure.insert(v)
        elif isinstance(structure, HashTable):
            structure.insert(v, v)
    end = time.time()
    return end - start

def benchmark_search(structure, values):
    start = time.time()
    for v in values:
        if isinstance(structure, BinaryHeap):
            # linear search for benchmarking only
            _ = v in structure.data
        elif isinstance(structure, AVLTree):
            structure.search(v)
        elif isinstance(structure, HashTable):
            structure.get(v)
    end = time.time()
    return end - start

def benchmark_delete(structure, values):
    start = time.time()
    for v in values:
        if isinstance(structure, BinaryHeap):
            # remove min/max depending on heap type
            if structure.is_min_heap:
                structure.extract_min()
            else:
                structure.extract_max()
        elif isinstance(structure, AVLTree):
            structure.delete(v)
        elif isinstance(structure, HashTable):
            structure.delete(v)
    end = time.time()
    return end - start

# -------------------- MAIN BENCHMARK --------------------
results = []

for size in SIZES:
    print(f"Benchmarking size: {size}")
    data = [random.randint(0, size*10) for _ in range(size)]

    # --- Binary Heap ---
    min_heap = BinaryHeap(is_min_heap=True)
    max_heap = BinaryHeap(is_min_heap=False)
    t_insert_min = benchmark_insert(min_heap, data)
    t_insert_max = benchmark_insert(max_heap, data)
    t_search_min = benchmark_search(min_heap, data[:100])
    t_search_max = benchmark_search(max_heap, data[:100])
    t_delete_min = benchmark_delete(min_heap, data)
    t_delete_max = benchmark_delete(max_heap, data)

    # --- AVL Tree ---
    avl = AVLTree()
    t_insert_avl = benchmark_insert(avl, data)
    t_search_avl = benchmark_search(avl, data)
    t_delete_avl = benchmark_delete(avl, data)

    # --- Hash Table (chaining) ---
    ht_chain = HashTable(method="chaining")
    t_insert_ht_chain = benchmark_insert(ht_chain, data)
    t_search_ht_chain = benchmark_search(ht_chain, data)
    t_delete_ht_chain = benchmark_delete(ht_chain, data)

    # --- Hash Table (linear probing) ---
    ht_linear = HashTable(method="linear")
    t_insert_ht_linear = benchmark_insert(ht_linear, data)
    t_search_ht_linear = benchmark_search(ht_linear, data)
    t_delete_ht_linear = benchmark_delete(ht_linear, data)

    # --- Collect results ---
    results.append([
        size,
        t_insert_min, t_insert_max, t_search_min, t_search_max, t_delete_min, t_delete_max,
        t_insert_avl, t_search_avl, t_delete_avl,
        t_insert_ht_chain, t_search_ht_chain, t_delete_ht_chain,
        t_insert_ht_linear, t_search_ht_linear, t_delete_ht_linear
    ])

# -------------------- WRITE CSV --------------------
with open(RESULTS_CSV, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow([
        "size",
        "insert_minheap", "insert_maxheap", "search_minheap", "search_maxheap", "delete_minheap", "delete_maxheap",
        "insert_avl", "search_avl", "delete_avl",
        "insert_ht_chain", "search_ht_chain", "delete_ht_chain",
        "insert_ht_linear", "search_ht_linear", "delete_ht_linear"
    ])
    writer.writerows(results)

# -------------------- PLOT RESULTS --------------------
sizes = [row[0] for row in results]

def plot_operation(op_index, op_name):
    plt.figure(figsize=(12,6))
    plt.plot(sizes, [row[op_index] for row in results], label="Heap Min/Insert" if "Insert" in op_name else "")
    plt.plot(sizes, [row[op_index+1] for row in results], label="Heap Max" if "Insert" in op_name else "")
    plt.plot(sizes, [row[7 + (op_index-1)//2] for row in results], label="AVL Tree")
    plt.plot(sizes, [row[10 + (op_index-1)//2] for row in results], label="HashTable Chaining")
    plt.plot(sizes, [row[13 + (op_index-1)//2] for row in results], label="HashTable Linear")
    plt.xlabel("Input Size")
    plt.ylabel("Time (s)")
    plt.title(f"Week 3 Structures - {op_name} Performance")
    plt.legend()
    plt.grid(True)
    plt.savefig(f"benchmarks/results/week3_structures_{op_name.lower()}.png")
    plt.show()

# Plot Insert, Search, Delete separately
plot_operation(1, "Insert")
plot_operation(3, "Search")
plot_operation(5, "Delete")
