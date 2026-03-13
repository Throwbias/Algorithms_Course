"""
Visualization helpers for Week 9 approximation benchmarks.
"""

import os
import pandas as pd
import matplotlib.pyplot as plt


def ensure_output_dir(path):
    os.makedirs(path, exist_ok=True)


def save_approx_ratio_plot(csv_path, output_path):
    df = pd.read_csv(csv_path)

    plt.figure(figsize=(10, 6))
    for algo in df["algorithm"].unique():
        subset = df[df["algorithm"] == algo]
        plt.plot(subset["input_size"], subset["approx_ratio"], marker="o", label=algo)

    plt.xlabel("Input Size")
    plt.ylabel("Approximation Ratio")
    plt.title("Approximation Ratios by Algorithm")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()


def save_cost_vs_optimal_plot(csv_path, output_path):
    df = pd.read_csv(csv_path)

    plt.figure(figsize=(10, 6))
    plt.plot(df.index, df["solution_value"], marker="o", label="Approximate Solution")
    plt.plot(df.index, df["optimum_value"], marker="s", label="Optimal Solution")

    plt.xlabel("Benchmark Instance")
    plt.ylabel("Cost / Value")
    plt.title("Approximate vs Optimal Solutions")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()


def save_randomized_maxcut_plot(df, output_path):
    subset = df[df["problem"] == "Max-Cut"]

    plt.figure(figsize=(10, 6))
    plt.plot(subset["input_size"], subset["solution_value"], marker="o", label="Randomized Best Cut")
    plt.plot(subset["input_size"], subset["optimum_value"], marker="s", label="Optimal Cut")

    plt.xlabel("Input Size")
    plt.ylabel("Cut Value")
    plt.title("Randomized Max-Cut Performance")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()