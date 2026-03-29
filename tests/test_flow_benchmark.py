import os
import pandas as pd
from benchmarks.week10_flow_benchmark import run_benchmarks


def test_flow_benchmark_generates_outputs():
    run_benchmarks()

    csv_path = os.path.join("benchmarks", "results", "flow_benchmark_results.csv")
    runtime_plot = os.path.join("benchmarks", "results", "flow_runtime_comparison.png")
    counts_plot = os.path.join("benchmarks", "results", "flow_algorithm_counts.png")

    assert os.path.exists(csv_path)
    assert os.path.exists(runtime_plot)
    assert os.path.exists(counts_plot)

    df = pd.read_csv(csv_path)
    assert len(df) > 0
    assert {"algorithm", "runtime_sec", "max_flow", "input_size", "density"}.issubset(df.columns)