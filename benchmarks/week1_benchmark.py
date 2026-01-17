import time
import csv
import os
import matplotlib.pyplot as plt
from src.sorting.basic_sorts import bubble_sort, selection_sort, insertion_sort

# Algorithms to benchmark
SORT_FUNCTIONS = {
    "bubble_sort": bubble_sort,
    "selection_sort": selection_sort,
    "insertion_sort": insertion_sort
}

# Input sizes and types
INPUT_SIZES = [100, 500, 1000, 5000]
INPUT_TYPES = ["random", "sorted", "reverse"]

RESULTS_DIR = "benchmarks/results"
os.makedirs(RESULTS_DIR, exist_ok=True)

def generate_data(size: int, data_type: str):
    import random
    if data_type == "random":
        return [random.randint(0, size) for _ in range(size)]
    elif data_type == "sorted":
        return list(range(size))
    elif data_type == "reverse":
        return list(range(size, 0, -1))
    else:
        raise ValueError(f"Unknown data type: {data_type}")

def benchmark():
    results = []

    for size in INPUT_SIZES:
        for data_type in INPUT_TYPES:
            data = generate_data(size, data_type)
            for name, func in SORT_FUNCTIONS.items():
                start = time.time()
                func(data)
                elapsed = time.time() - start
                results.append([name, data_type, size, elapsed])
                print(f"{name} | {data_type} | {size} -> {elapsed:.6f}s")

    # Save CSV
    csv_file = os.path.join(RESULTS_DIR, "week1_results.csv")
    with open(csv_file, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["algorithm", "data_type", "size", "time"])
        writer.writerows(results)
    print(f"Results saved to {csv_file}")

    # Plot
    for data_type in INPUT_TYPES:
        plt.figure()
        for name in SORT_FUNCTIONS:
            times = [r[3] for r in results if r[0] == name and r[1] == data_type]
            plt.plot(INPUT_SIZES, times, marker="o", label=name)
        plt.title(f"Sorting Performance - {data_type} data")
        plt.xlabel("Input size")
        plt.ylabel("Time (s)")
        plt.legend()
        plt.grid(True)
        plt.savefig(os.path.join(RESULTS_DIR, f"{data_type}_plot.png"))
        plt.close()
        print(f"Plot saved for {data_type} data")
    
    print("Benchmarking complete!")

if __name__ == "__main__":
    benchmark()
