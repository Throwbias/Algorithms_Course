"""
String Search Benchmark

Compares:
- KMP
- Rabin-Karp
- Suffix Array
- Suffix Tree

Outputs:
- benchmarks/results/string_benchmark_results.csv
- benchmarks/results/runtime_comparison.png
- benchmarks/results/sa_lcp_stats.png
- benchmarks/results/heatmap_dataset_sizes.png
- benchmarks/results/collision_analysis.png
"""

import os
import sys
import time
import random
import pandas as pd
import matplotlib.pyplot as plt

# Ensure repo root is importable
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.strings.kmp import kmp_search_all
from src.strings.rabin_karp import rabin_karp_search_all, rolling_hash
from src.strings.suffix_array import build_suffix_array, build_lcp_array, suffix_array_search
from src.strings.suffix_tree import CompressedSuffixTree


RESULTS_DIR = os.path.join("benchmarks", "results")
CSV_PATH = os.path.join(RESULTS_DIR, "string_benchmark_results.csv")


def ensure_output_dir(path):
    os.makedirs(path, exist_ok=True)


def generate_synthetic_text(length, alphabet="abcd", seed=42):
    rng = random.Random(seed)
    return "".join(rng.choice(alphabet) for _ in range(length))


def inject_pattern(text, pattern, interval):
    chars = list(text)
    i = 0
    while i + len(pattern) <= len(chars):
        chars[i:i + len(pattern)] = list(pattern)
        i += interval
    return "".join(chars)


def benchmark_kmp(text, pattern):
    start = time.perf_counter()
    matches = kmp_search_all(text, pattern)
    runtime = time.perf_counter() - start
    return {
        "algorithm": "KMP",
        "preprocessing_time_sec": 0.0,
        "search_time_sec": runtime,
        "total_time_sec": runtime,
        "match_count": len(matches),
    }


def benchmark_rabin_karp(text, pattern):
    start = time.perf_counter()
    matches = rabin_karp_search_all(text, pattern)
    runtime = time.perf_counter() - start
    return {
        "algorithm": "Rabin-Karp",
        "preprocessing_time_sec": 0.0,
        "search_time_sec": runtime,
        "total_time_sec": runtime,
        "match_count": len(matches),
    }


def benchmark_suffix_array(text, pattern):
    build_start = time.perf_counter()
    sa = build_suffix_array(text)
    lcp = build_lcp_array(text, sa)
    build_time = time.perf_counter() - build_start

    search_start = time.perf_counter()
    matches = suffix_array_search(text, pattern, sa)
    search_time = time.perf_counter() - search_start

    avg_lcp = sum(lcp) / len(lcp) if lcp else 0.0
    max_lcp = max(lcp) if lcp else 0

    return {
        "algorithm": "Suffix Array",
        "preprocessing_time_sec": build_time,
        "search_time_sec": search_time,
        "total_time_sec": build_time + search_time,
        "match_count": len(matches),
        "avg_lcp": avg_lcp,
        "max_lcp": max_lcp,
    }


def benchmark_suffix_tree(text, pattern):
    build_start = time.perf_counter()
    tree = CompressedSuffixTree(text)
    build_time = time.perf_counter() - build_start

    search_start = time.perf_counter()
    matches = tree.search(pattern)
    search_time = time.perf_counter() - search_start

    return {
        "algorithm": "Suffix Tree",
        "preprocessing_time_sec": build_time,
        "search_time_sec": search_time,
        "total_time_sec": build_time + search_time,
        "match_count": len(matches),
    }


def rabin_karp_collision_experiment(lengths, pattern_length=6, alphabet="abcd", modulus_values=None):
    """
    Estimate hash collisions by comparing distinct windows against distinct hash values.
    A collision here means two different substrings share the same hash.
    """
    if modulus_values is None:
        modulus_values = [5, 11, 101, 1009]

    rows = []

    for length in lengths:
        text = generate_synthetic_text(length, alphabet=alphabet, seed=900 + length)

        if length < pattern_length:
            continue

        windows = [text[i:i + pattern_length] for i in range(length - pattern_length + 1)]
        distinct_windows = set(windows)

        for modulus in modulus_values:
            hashes = {}
            collision_count = 0

            for window in distinct_windows:
                h = rolling_hash(window, modulus=modulus)
                if h in hashes and hashes[h] != window:
                    collision_count += 1
                else:
                    hashes[h] = window

            rows.append({
                "dataset_size": length,
                "modulus": modulus,
                "pattern_length": pattern_length,
                "distinct_windows": len(distinct_windows),
                "collision_count": collision_count,
                "collision_rate": collision_count / len(distinct_windows) if distinct_windows else 0.0,
            })

    return pd.DataFrame(rows)


def run_benchmarks():
    ensure_output_dir(RESULTS_DIR)

    rows = []
    sizes = [1_000, 5_000, 10_000, 25_000]
    pattern = "abca"

    for size in sizes:
        seed = 100 + size
        base_text = generate_synthetic_text(size, alphabet="abcd", seed=seed)
        text = inject_pattern(base_text, pattern, interval=max(50, size // 20))

        kmp_result = benchmark_kmp(text, pattern)
        kmp_result["dataset_size"] = size
        rows.append(kmp_result)

        rk_result = benchmark_rabin_karp(text, pattern)
        rk_result["dataset_size"] = size
        rows.append(rk_result)

        sa_result = benchmark_suffix_array(text, pattern)
        sa_result["dataset_size"] = size
        rows.append(sa_result)

        tree_result = benchmark_suffix_tree(text, pattern)
        tree_result["dataset_size"] = size
        rows.append(tree_result)

        print(
            f"Completed size={size} | "
            f"KMP={kmp_result['total_time_sec']:.6f}s, "
            f"RK={rk_result['total_time_sec']:.6f}s, "
            f"SA={sa_result['total_time_sec']:.6f}s, "
            f"TREE={tree_result['total_time_sec']:.6f}s"
        )

    df = pd.DataFrame(rows)
    df.to_csv(CSV_PATH, index=False)

    collision_df = rabin_karp_collision_experiment(sizes)
    collision_df.to_csv(os.path.join(RESULTS_DIR, "collision_analysis.csv"), index=False)

    save_runtime_plot(df)
    save_sa_lcp_plot(df)
    save_heatmap(df)
    save_collision_plot(collision_df)

    print(f"\nSaved CSV: {CSV_PATH}")
    print(f"Saved CSV: {os.path.join(RESULTS_DIR, 'collision_analysis.csv')}")
    print(f"Saved plot: {os.path.join(RESULTS_DIR, 'runtime_comparison.png')}")
    print(f"Saved plot: {os.path.join(RESULTS_DIR, 'sa_lcp_stats.png')}")
    print(f"Saved plot: {os.path.join(RESULTS_DIR, 'heatmap_dataset_sizes.png')}")
    print(f"Saved plot: {os.path.join(RESULTS_DIR, 'collision_analysis.png')}")
    print("\nBenchmark preview:")
    print(df.head())


def save_runtime_plot(df):
    plt.figure(figsize=(10, 6))

    for algorithm in df["algorithm"].unique():
        subset = df[df["algorithm"] == algorithm].sort_values("dataset_size")
        plt.plot(
            subset["dataset_size"],
            subset["total_time_sec"],
            marker="o",
            label=algorithm,
        )

    plt.xlabel("Dataset Size (characters)")
    plt.ylabel("Total Time (seconds)")
    plt.title("String Search Runtime Comparison")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(RESULTS_DIR, "runtime_comparison.png"))
    plt.close()


def save_sa_lcp_plot(df):
    sa_df = df[df["algorithm"] == "Suffix Array"].sort_values("dataset_size")

    plt.figure(figsize=(10, 6))
    plt.plot(sa_df["dataset_size"], sa_df["avg_lcp"], marker="o", label="Average LCP")
    plt.plot(sa_df["dataset_size"], sa_df["max_lcp"], marker="s", label="Maximum LCP")
    plt.xlabel("Dataset Size (characters)")
    plt.ylabel("LCP Value")
    plt.title("Suffix Array LCP Statistics")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(RESULTS_DIR, "sa_lcp_stats.png"))
    plt.close()


def save_heatmap(df):
    pivot = df.pivot(index="algorithm", columns="dataset_size", values="total_time_sec")

    plt.figure(figsize=(10, 4))
    plt.imshow(pivot.values, aspect="auto")
    plt.xticks(range(len(pivot.columns)), pivot.columns)
    plt.yticks(range(len(pivot.index)), pivot.index)
    plt.colorbar(label="Total Time (seconds)")
    plt.title("Search Runtime Heatmap by Dataset Size")
    plt.xlabel("Dataset Size")
    plt.ylabel("Algorithm")
    plt.tight_layout()
    plt.savefig(os.path.join(RESULTS_DIR, "heatmap_dataset_sizes.png"))
    plt.close()


def save_collision_plot(collision_df):
    plt.figure(figsize=(10, 6))

    for modulus in sorted(collision_df["modulus"].unique()):
        subset = collision_df[collision_df["modulus"] == modulus].sort_values("dataset_size")
        plt.plot(
            subset["dataset_size"],
            subset["collision_rate"],
            marker="o",
            label=f"modulus={modulus}",
        )

    plt.xlabel("Dataset Size (characters)")
    plt.ylabel("Collision Rate")
    plt.title("Rabin-Karp Collision Analysis")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(RESULTS_DIR, "collision_analysis.png"))
    plt.close()


if __name__ == "__main__":
    run_benchmarks()