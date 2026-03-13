"""
Week 9 Approximation Benchmark

Benchmarks:
- Vertex Cover 2-Approx
- Set Cover LP Rounding / Greedy fallback
- Facility Location Greedy
- Metric TSP 2-Approx
- Randomized Max-Cut

Outputs:
- benchmarks/results/comparison_table.csv
- benchmarks/results/approx_ratios.png
- benchmarks/results/cost_vs_optimal.png
- benchmarks/results/randomized_maxcut_results.png
"""

import os
import sys
import time
import pandas as pd

# Ensure repo root is importable
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.approximation.vertex_cover_2approx import vertex_cover_2approx, exact_min_vertex_cover
from src.approximation.set_cover_lpround import set_cover_lp_relaxation_rounding, exact_set_cover
from src.approximation.facility_location_greedy import greedy_facility_location, exact_facility_location
from src.approximation.tsp_metric_approx import tsp_metric_approx, exact_tsp
from src.approximation.maxcut_randomized import randomized_maxcut, exact_maxcut

from src.utils.graph_utils import (
    generate_random_graph,
    generate_metric_points,
    generate_set_cover_instance,
    generate_facility_location_instance,
)
from src.utils.visualization import (
    ensure_output_dir,
    save_approx_ratio_plot,
    save_cost_vs_optimal_plot,
    save_randomized_maxcut_plot,
)


RESULTS_DIR = os.path.join("benchmarks", "results")
CSV_PATH = os.path.join(RESULTS_DIR, "comparison_table.csv")


def benchmark_vertex_cover():
    rows = []
    for n in [6, 8, 10]:
        vertices, edges = generate_random_graph(n, edge_probability=0.35, seed=100 + n)

        start = time.perf_counter()
        approx_cover = vertex_cover_2approx(edges)
        runtime = time.perf_counter() - start

        optimum_cover = exact_min_vertex_cover(edges)

        approx_value = len(approx_cover)
        optimum_value = len(optimum_cover)
        ratio = approx_value / optimum_value if optimum_value > 0 else 1.0

        rows.append({
            "problem": "Vertex Cover",
            "algorithm": "2-Approx",
            "input_size": n,
            "runtime_sec": runtime,
            "solution_value": approx_value,
            "optimum_value": optimum_value,
            "approx_ratio": ratio
        })
    return rows


def benchmark_set_cover():
    rows = []
    for size in [6, 8, 10]:
        universe, sets, costs = generate_set_cover_instance(universe_size=size, num_sets=size + 2, seed=200 + size)

        start = time.perf_counter()
        approx_result = set_cover_lp_relaxation_rounding(universe, sets, costs)
        runtime = time.perf_counter() - start

        optimum_result = exact_set_cover(universe, sets, costs)

        approx_value = approx_result["total_cost"]
        optimum_value = optimum_result["total_cost"]
        ratio = approx_value / optimum_value if optimum_value > 0 else 1.0

        rows.append({
            "problem": "Set Cover",
            "algorithm": approx_result.get("method", "LP-Rounding"),
            "input_size": size,
            "runtime_sec": runtime,
            "solution_value": approx_value,
            "optimum_value": optimum_value,
            "approx_ratio": ratio
        })
    return rows


def benchmark_facility_location():
    rows = []
    for size in [3, 4, 5]:
        opening_costs, assignment_costs = generate_facility_location_instance(
            num_facilities=size,
            num_clients=size + 2,
            seed=300 + size
        )

        start = time.perf_counter()
        approx_result = greedy_facility_location(opening_costs, assignment_costs)
        runtime = time.perf_counter() - start

        optimum_result = exact_facility_location(opening_costs, assignment_costs)

        approx_value = approx_result["total_cost"]
        optimum_value = optimum_result["total_cost"]
        ratio = approx_value / optimum_value if optimum_value > 0 else 1.0

        rows.append({
            "problem": "Facility Location",
            "algorithm": "Greedy",
            "input_size": size,
            "runtime_sec": runtime,
            "solution_value": approx_value,
            "optimum_value": optimum_value,
            "approx_ratio": ratio
        })
    return rows


def benchmark_tsp():
    rows = []
    for n in [5, 6, 7]:
        points = generate_metric_points(n, seed=400 + n)

        start = time.perf_counter()
        approx_result = tsp_metric_approx(points)
        runtime = time.perf_counter() - start

        optimum_result = exact_tsp(points)

        approx_value = approx_result["cost"]
        optimum_value = optimum_result["cost"]
        ratio = approx_value / optimum_value if optimum_value > 0 else 1.0

        rows.append({
            "problem": "Metric TSP",
            "algorithm": "MST Preorder 2-Approx",
            "input_size": n,
            "runtime_sec": runtime,
            "solution_value": approx_value,
            "optimum_value": optimum_value,
            "approx_ratio": ratio
        })
    return rows


def benchmark_maxcut():
    rows = []
    for n in [6, 8, 10]:
        vertices, edges = generate_random_graph(n, edge_probability=0.4, seed=500 + n)

        start = time.perf_counter()
        approx_result = randomized_maxcut(vertices, edges, trials=200, seed=123 + n)
        runtime = time.perf_counter() - start

        optimum_result = exact_maxcut(vertices, edges)

        approx_value = approx_result["cut_value"]
        optimum_value = optimum_result["cut_value"]
        ratio = optimum_value / approx_value if approx_value > 0 else float("inf")

        rows.append({
            "problem": "Max-Cut",
            "algorithm": "Randomized",
            "input_size": n,
            "runtime_sec": runtime,
            "solution_value": approx_value,
            "optimum_value": optimum_value,
            "approx_ratio": ratio
        })
    return rows


def run_benchmarks():
    ensure_output_dir(RESULTS_DIR)

    rows = []
    rows.extend(benchmark_vertex_cover())
    rows.extend(benchmark_set_cover())
    rows.extend(benchmark_facility_location())
    rows.extend(benchmark_tsp())
    rows.extend(benchmark_maxcut())

    df = pd.DataFrame(rows)
    df.to_csv(CSV_PATH, index=False)

    save_approx_ratio_plot(CSV_PATH, os.path.join(RESULTS_DIR, "approx_ratios.png"))
    save_cost_vs_optimal_plot(CSV_PATH, os.path.join(RESULTS_DIR, "cost_vs_optimal.png"))
    save_randomized_maxcut_plot(df, os.path.join(RESULTS_DIR, "randomized_maxcut_results.png"))

    print(f"Saved CSV: {CSV_PATH}")
    print(f"Saved plot: {os.path.join(RESULTS_DIR, 'approx_ratios.png')}")
    print(f"Saved plot: {os.path.join(RESULTS_DIR, 'cost_vs_optimal.png')}")
    print(f"Saved plot: {os.path.join(RESULTS_DIR, 'randomized_maxcut_results.png')}")
    print(df)


if __name__ == "__main__":
    run_benchmarks()