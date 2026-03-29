import os
import pandas as pd
from benchmarks.benchmark_search import run_benchmarks


def test_string_benchmark_generates_outputs():
    run_benchmarks()

    csv_path = os.path.join("benchmarks", "results", "string_benchmark_results.csv")
    collision_csv = os.path.join("benchmarks", "results", "collision_analysis.csv")
    runtime_plot = os.path.join("benchmarks", "results", "runtime_comparison.png")
    lcp_plot = os.path.join("benchmarks", "results", "sa_lcp_stats.png")
    heatmap_plot = os.path.join("benchmarks", "results", "heatmap_dataset_sizes.png")
    collision_plot = os.path.join("benchmarks", "results", "collision_analysis.png")

    assert os.path.exists(csv_path)
    assert os.path.exists(collision_csv)
    assert os.path.exists(runtime_plot)
    assert os.path.exists(lcp_plot)
    assert os.path.exists(heatmap_plot)
    assert os.path.exists(collision_plot)

    df = pd.read_csv(csv_path)
    assert len(df) > 0
    assert {
        "algorithm",
        "dataset_size",
        "preprocessing_time_sec",
        "search_time_sec",
        "total_time_sec",
        "match_count",
    }.issubset(df.columns)

    assert "Suffix Tree" in set(df["algorithm"])

    collision_df = pd.read_csv(collision_csv)
    assert len(collision_df) > 0
    assert {
        "dataset_size",
        "modulus",
        "collision_count",
        "collision_rate",
    }.issubset(collision_df.columns)