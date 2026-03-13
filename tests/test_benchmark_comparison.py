import os
import pandas as pd
from benchmarks.week9_approx_benchmark import run_benchmarks


def test_benchmark_generates_csv():
    run_benchmarks()
    csv_path = os.path.join("benchmarks", "results", "comparison_table.csv")

    assert os.path.exists(csv_path)

    df = pd.read_csv(csv_path)
    required_columns = {
        "problem",
        "algorithm",
        "input_size",
        "runtime_sec",
        "solution_value",
        "optimum_value",
        "approx_ratio",
    }

    assert required_columns.issubset(df.columns)
    assert len(df) > 0