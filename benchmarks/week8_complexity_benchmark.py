"""
Week 8 Complexity Benchmark

Benchmarks:
- Subset Sum backtracking vs greedy heuristic
- SAT backtracking vs random heuristic
- Vertex Cover 2-approximation
- TSP nearest-neighbor heuristic

Outputs:
- benchmarks/results/runtime_growth.png
- benchmarks/results/approximation_quality.png
- benchmarks/results/comparison_table.csv
"""

import os
import sys
import csv
import math
import time
import random
import itertools
import matplotlib.pyplot as plt

# Ensure project root is importable
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.complexity.subset_sum_backtracking import (
    subset_sum_backtracking,
    subset_sum_greedy,
)
from src.complexity.satisfiability_solver import (
    solve_sat_backtracking,
    random_sat_heuristic,
)
from src.complexity.vertex_cover_approx import (
    vertex_cover_approx,
    is_vertex_cover,
)
from src.complexity.traveling_salesman_approx import tsp_nearest_neighbor
from src.utils.timer import time_function


RESULTS_DIR = os.path.join("benchmarks", "results")
CSV_PATH = os.path.join(RESULTS_DIR, "comparison_table.csv")
RUNTIME_PLOT = os.path.join(RESULTS_DIR, "runtime_growth.png")
QUALITY_PLOT = os.path.join(RESULTS_DIR, "approximation_quality.png")


def ensure_results_dir():
    os.makedirs(RESULTS_DIR, exist_ok=True)


# ----------------------------
# Helpers
# ----------------------------

def path_length(points, path):
    total = 0.0
    for i in range(len(path) - 1):
        a = points[path[i]]
        b = points[path[i + 1]]
        total += math.dist(a, b)
    return total


def brute_force_tsp(points):
    n = len(points)
    best_path = None
    best_cost = float("inf")

    for perm in itertools.permutations(range(1, n)):
        path = [0] + list(perm) + [0]
        cost = path_length(points, path)
        if cost < best_cost:
            best_cost = cost
            best_path = path

    return best_path, best_cost


def generate_random_graph(num_vertices, edge_prob=0.3):
    edges = set()
    vertices = list(range(num_vertices))
    for i in range(num_vertices):
        for j in range(i + 1, num_vertices):
            if random.random() < edge_prob:
                edges.add((vertices[i], vertices[j]))

    if not edges and num_vertices >= 2:
        edges.add((0, 1))
    return vertices, edges


def brute_force_min_vertex_cover(vertices, edges):
    for r in range(len(vertices) + 1):
        for subset in itertools.combinations(vertices, r):
            cover = set(subset)
            if is_vertex_cover(edges, cover):
                return cover
    return set(vertices)


def random_cnf(num_vars, num_clauses, clause_size=3):
    cnf = []
    for _ in range(num_clauses):
        vars_in_clause = random.sample(range(1, num_vars + 1), min(clause_size, num_vars))
        clause = []
        for v in vars_in_clause:
            literal = v if random.choice([True, False]) else -v
            clause.append(literal)
        cnf.append(clause)
    return cnf


# ----------------------------
# Benchmarks
# ----------------------------

def benchmark_subset_sum(rows):
    sizes = [10, 12, 14, 16, 18]

    for n in sizes:
        nums = [random.randint(1, 25) for _ in range(n)]
        target = sum(nums) // 2

        exact_result, exact_time = time_function(subset_sum_backtracking, nums, target)
        greedy_result, greedy_time = time_function(subset_sum_greedy, nums, target)

        exact_value = sum(exact_result) if exact_result else None
        greedy_value = sum(greedy_result) if greedy_result else 0

        rows.append({
            "problem": "Subset Sum",
            "algorithm": "Backtracking",
            "input_size": n,
            "runtime_sec": exact_time,
            "solution_value": exact_value,
            "optimum_value": target if exact_result else None,
            "approx_ratio": 1.0 if exact_result else None,
        })

        rows.append({
            "problem": "Subset Sum",
            "algorithm": "Greedy",
            "input_size": n,
            "runtime_sec": greedy_time,
            "solution_value": greedy_value,
            "optimum_value": target if exact_result else None,
            "approx_ratio": (greedy_value / target) if target > 0 else None,
        })


def benchmark_sat(rows):
    sizes = [4, 5, 6, 7, 8]

    for num_vars in sizes:
        cnf = random_cnf(num_vars=num_vars, num_clauses=num_vars + 2)

        exact_result, exact_time = time_function(solve_sat_backtracking, cnf, num_vars)
        heuristic_result, heuristic_time = time_function(random_sat_heuristic, cnf, num_vars, 500)

        rows.append({
            "problem": "SAT",
            "algorithm": "Backtracking",
            "input_size": num_vars,
            "runtime_sec": exact_time,
            "solution_value": 1 if exact_result is not None else 0,
            "optimum_value": 1 if exact_result is not None else 0,
            "approx_ratio": 1.0 if exact_result is not None else 0.0,
        })

        rows.append({
            "problem": "SAT",
            "algorithm": "Random Heuristic",
            "input_size": num_vars,
            "runtime_sec": heuristic_time,
            "solution_value": 1 if heuristic_result is not None else 0,
            "optimum_value": 1 if exact_result is not None else 0,
            "approx_ratio": (
                (1 if heuristic_result is not None else 0) /
                (1 if exact_result is not None else 1)
            ),
        })


def benchmark_vertex_cover(rows):
    sizes = [6, 7, 8, 9, 10]

    for n in sizes:
        vertices, edges = generate_random_graph(n, edge_prob=0.35)

        approx_cover, approx_time = time_function(vertex_cover_approx, edges)
        optimal_cover, optimal_time = time_function(brute_force_min_vertex_cover, vertices, edges)

        approx_size = len(approx_cover)
        optimal_size = len(optimal_cover)
        ratio = (approx_size / optimal_size) if optimal_size > 0 else 1.0

        rows.append({
            "problem": "Vertex Cover",
            "algorithm": "2-Approximation",
            "input_size": n,
            "runtime_sec": approx_time,
            "solution_value": approx_size,
            "optimum_value": optimal_size,
            "approx_ratio": ratio,
        })

        rows.append({
            "problem": "Vertex Cover",
            "algorithm": "Optimal (Brute Force)",
            "input_size": n,
            "runtime_sec": optimal_time,
            "solution_value": optimal_size,
            "optimum_value": optimal_size,
            "approx_ratio": 1.0,
        })


def benchmark_tsp(rows):
    sizes = [5, 6, 7, 8]

    for n in sizes:
        points = [(random.uniform(0, 100), random.uniform(0, 100)) for _ in range(n)]

        heuristic_path, heuristic_time = time_function(tsp_nearest_neighbor, points)
        heuristic_cost = path_length(points, heuristic_path)

        optimal_result, optimal_time = time_function(brute_force_tsp, points)
        optimal_path, optimal_cost = optimal_result

        ratio = heuristic_cost / optimal_cost if optimal_cost > 0 else 1.0

        rows.append({
            "problem": "TSP",
            "algorithm": "Nearest Neighbor",
            "input_size": n,
            "runtime_sec": heuristic_time,
            "solution_value": heuristic_cost,
            "optimum_value": optimal_cost,
            "approx_ratio": ratio,
        })

        rows.append({
            "problem": "TSP",
            "algorithm": "Optimal (Brute Force)",
            "input_size": n,
            "runtime_sec": optimal_time,
            "solution_value": optimal_cost,
            "optimum_value": optimal_cost,
            "approx_ratio": 1.0,
        })


# ----------------------------
# Output
# ----------------------------

def write_csv(rows):
    fieldnames = [
        "problem",
        "algorithm",
        "input_size",
        "runtime_sec",
        "solution_value",
        "optimum_value",
        "approx_ratio",
    ]

    with open(CSV_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def plot_runtime_growth(rows):
    grouped = {}
    for row in rows:
        key = (row["problem"], row["algorithm"])
        grouped.setdefault(key, {"x": [], "y": []})
        grouped[key]["x"].append(row["input_size"])
        grouped[key]["y"].append(row["runtime_sec"])

    plt.figure(figsize=(10, 6))
    for (problem, algorithm), data in grouped.items():
        plt.plot(data["x"], data["y"], marker="o", label=f"{problem} - {algorithm}")

    plt.xlabel("Input Size")
    plt.ylabel("Runtime (seconds)")
    plt.title("Week 8 Runtime Growth: Exact vs Heuristic/Approximate Methods")
    plt.legend()
    plt.tight_layout()
    plt.savefig(RUNTIME_PLOT)
    plt.close()


def plot_approximation_quality(rows):
    filtered = [
        row for row in rows
        if row["problem"] in {"Vertex Cover", "TSP"} and row["algorithm"] not in {"Optimal (Brute Force)"}
    ]

    grouped = {}
    for row in filtered:
        key = (row["problem"], row["algorithm"])
        grouped.setdefault(key, {"x": [], "y": []})
        grouped[key]["x"].append(row["input_size"])
        grouped[key]["y"].append(row["approx_ratio"])

    plt.figure(figsize=(10, 6))
    for (problem, algorithm), data in grouped.items():
        plt.plot(data["x"], data["y"], marker="o", label=f"{problem} - {algorithm}")

    plt.xlabel("Input Size")
    plt.ylabel("Approximation Ratio")
    plt.title("Approximation Quality vs Input Size")
    plt.legend()
    plt.tight_layout()
    plt.savefig(QUALITY_PLOT)
    plt.close()


def main():
    random.seed(42)
    ensure_results_dir()

    rows = []
    benchmark_subset_sum(rows)
    benchmark_sat(rows)
    benchmark_vertex_cover(rows)
    benchmark_tsp(rows)

    write_csv(rows)
    plot_runtime_growth(rows)
    plot_approximation_quality(rows)

    print(f"Saved CSV: {CSV_PATH}")
    print(f"Saved plot: {RUNTIME_PLOT}")
    print(f"Saved plot: {QUALITY_PLOT}")


if __name__ == "__main__":
    main()