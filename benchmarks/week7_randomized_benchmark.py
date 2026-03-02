import os
import sys
import time
import random
import csv
import math
import statistics as stats
import matplotlib.pyplot as plt

# --- Ensure repo root is on path ---
# This file lives in: <repo_root>/benchmarks/week7_randomized_benchmark.py
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Part 1 imports
from src.sorting.deterministic_quick_sort import deterministic_quick_sort
from src.randomized.randomized_quicksort import randomized_quicksort, QuickSortStats

# Part 2 imports
from src.randomized.randomized_selection import randomized_selection, QuickSelectStats

# Part 3 imports (robust to naming differences)
try:
    from src.randomized.montecarlo_primality import (
        is_prime_trial_division,
        fermat_primality,
        miller_rabin_primality,
    )
except ImportError:
    # fallback: some versions name the deterministic baseline differently
    from src.randomized.montecarlo_primality import (
        is_prime_deterministic as is_prime_trial_division,
        fermat_primality,
        miller_rabin_primality,
    )

# Part 4 imports
from src.randomized.bloom_filter import BloomFilter

# Part 5 imports
from src.randomized.minhash_similarity import jaccard_similarity, minhash_estimate


def _time_one(fn, *args, **kwargs):
    t0 = time.perf_counter()
    fn(*args, **kwargs)
    t1 = time.perf_counter()
    return t1 - t0


def _mean_var(times):
    if len(times) == 1:
        return times[0], 0.0
    return stats.mean(times), stats.pvariance(times)


def benchmark_time(fn, make_args, repeats=10):
    """
    make_args() -> (args_tuple, kwargs_dict)
    """
    times = []
    for _ in range(repeats):
        args, kwargs = make_args()
        times.append(_time_one(fn, *args, **kwargs))
    return _mean_var(times)


def deterministic_select_by_sort(arr, k):
    return sorted(arr)[k]


def _write_row(writer, section, n, input_type, det_mean, det_var, rnd_mean, rnd_var, det_aux="", rnd_aux=""):
    writer.writerow([section, n, input_type, det_mean, det_var, rnd_mean, rnd_var, det_aux, rnd_aux])


def main():
    random.seed(42)

    out_dir = os.path.join("benchmarks", "results")
    os.makedirs(out_dir, exist_ok=True)

    summary_csv = os.path.join(out_dir, "summary_table.csv")

    with open(summary_csv, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["section", "n", "input_type", "det_mean_s", "det_var", "rnd_mean_s", "rnd_var", "det_aux", "rnd_aux"])

        # ============================================================
        # Part 1: Randomized QuickSort vs Deterministic (fixed pivot)
        # ============================================================
        sizes = [100, 300, 1000, 3000, 10_000, 30_000, 100_000]
        repeats_random = 15
        repeats_sorted = 5

        det_means_random, rnd_means_random = [], []
        det_means_sorted, rnd_means_sorted = [], []

        for n in sizes:
            base = [random.randint(0, 10**9) for _ in range(n)]
            sorted_input = sorted(base)

            det_mean_r, det_var_r = benchmark_time(
                deterministic_quick_sort,
                lambda b=base: ((b,), {}),
                repeats=repeats_random,
            )
            rnd_mean_r, rnd_var_r = benchmark_time(
                randomized_quicksort,
                lambda b=base: ((b,), {}),
                repeats=repeats_random,
            )

            det_mean_s, det_var_s = benchmark_time(
                deterministic_quick_sort,
                lambda s=sorted_input: ((s,), {}),
                repeats=repeats_sorted,
            )
            rnd_mean_s, rnd_var_s = benchmark_time(
                randomized_quicksort,
                lambda s=sorted_input: ((s,), {}),
                repeats=repeats_sorted,
            )

            det_means_random.append(det_mean_r)
            rnd_means_random.append(rnd_mean_r)
            det_means_sorted.append(det_mean_s)
            rnd_means_sorted.append(rnd_mean_s)

            _write_row(w, "quicksort", n, "random", det_mean_r, det_var_r, rnd_mean_r, rnd_var_r)
            _write_row(w, "quicksort", n, "sorted", det_mean_s, det_var_s, rnd_mean_s, rnd_var_s)

            print(
                f"[QuickSort] n={n:6d} | random det={det_mean_r:.6f}s rnd={rnd_mean_r:.6f}s "
                f"| sorted det={det_mean_s:.6f}s rnd={rnd_mean_s:.6f}s"
            )

        # Plot: random input comparison (log-log)
        plt.figure()
        plt.plot(sizes, det_means_random, label="Deterministic QuickSort (fixed pivot)")
        plt.plot(sizes, rnd_means_random, label="Randomized QuickSort")
        plt.xscale("log")
        plt.yscale("log")
        plt.xlabel("n (log scale)")
        plt.ylabel("Mean runtime (seconds, log scale)")
        plt.title("QuickSort runtime on random input")
        plt.legend()
        fig_qs = os.path.join(out_dir, "quicksort_comparison.png")
        plt.savefig(fig_qs, dpi=200, bbox_inches="tight")
        print(f"Saved plot: {fig_qs}")

        # Plot: sorted input comparison (log-log)
        plt.figure()
        plt.plot(sizes, det_means_sorted, label="Deterministic QuickSort (fixed pivot)")
        plt.plot(sizes, rnd_means_sorted, label="Randomized QuickSort")
        plt.xscale("log")
        plt.yscale("log")
        plt.xlabel("n (log scale)")
        plt.ylabel("Mean runtime (seconds, log scale)")
        plt.title("QuickSort runtime on sorted (adversarial) input")
        plt.legend()
        fig_qs_sorted = os.path.join(out_dir, "quicksort_comparison_sorted.png")
        plt.savefig(fig_qs_sorted, dpi=200, bbox_inches="tight")
        print(f"Saved plot: {fig_qs_sorted}")

        # Expected vs empirical comparisons (for report)
        for n in [1000, 5000, 10_000]:
            demo = [random.randint(0, 10**9) for _ in range(n)]
            st = QuickSortStats()
            randomized_quicksort(demo, seed=123, stats=st)
            baseline = n * math.log2(n)
            ratio = st.comparisons / baseline if baseline else 0.0
            _write_row(w, "quicksort_comparisons", n, "random", "", "", "", "", f"{st.comparisons}", f"{ratio:.3f}")
            print(
                f"[Comparisons] n={n:,} | empirical={st.comparisons:,} | "
                f"n log2 n≈{int(baseline):,} | ratio≈{ratio:.2f}"
            )

        # ============================================================
        # Part 2: Randomized Selection (QuickSelect)
        # ============================================================
        sel_sizes = [100, 300, 1000, 3000, 10_000, 30_000]
        sel_repeats = 30

        k_cases = [
            ("min", lambda n: 0),
            ("median", lambda n: n // 2),
            ("max", lambda n: n - 1),
        ]

        median_det_means = []
        median_rnd_means = []

        for n in sel_sizes:
            base = [random.randint(0, 10**9) for _ in range(n)]

            for label, k_fn in k_cases:
                k = k_fn(n)

                det_mean, det_var = benchmark_time(
                    deterministic_select_by_sort,
                    lambda b=base, kk=k: ((b, kk), {}),
                    repeats=sel_repeats,
                )

                depths = []

                def _run_rnd_selection(b, kk):
                    st = QuickSelectStats()
                    randomized_selection(b, kk, seed=None, stats=st)
                    depths.append(st.max_depth)

                rnd_mean, rnd_var = benchmark_time(
                    _run_rnd_selection,
                    lambda b=base, kk=k: ((b, kk), {}),
                    repeats=sel_repeats,
                )

                avg_depth = stats.mean(depths) if depths else 0.0

                _write_row(w, "selection", n, label, det_mean, det_var, rnd_mean, rnd_var, "", f"avgDepth={avg_depth:.2f}")

                if label == "median":
                    median_det_means.append(det_mean)
                    median_rnd_means.append(rnd_mean)

                print(
                    f"[Select] n={n:6d} k={label:6s} | det(sort)={det_mean:.6f}s rnd={rnd_mean:.6f}s "
                    f"| avgDepth={avg_depth:.2f}"
                )

        plt.figure()
        plt.plot(sel_sizes, median_det_means, label="Deterministic (sorted()[k])")
        plt.plot(sel_sizes, median_rnd_means, label="Randomized QuickSelect (median k)")
        plt.xscale("log")
        plt.yscale("log")
        plt.xlabel("n (log scale)")
        plt.ylabel("Mean runtime (seconds, log scale)")
        plt.title("Selection runtime: deterministic vs randomized (median k)")
        plt.legend()
        fig_sel = os.path.join(out_dir, "selection_runtime.png")
        plt.savefig(fig_sel, dpi=200, bbox_inches="tight")
        print(f"Saved plot: {fig_sel}")

        # ============================================================
        # Part 3: Monte Carlo Primality (Fermat vs Miller–Rabin)
        # ============================================================
        k_values = [5, 10, 20]

        composites = [
            9, 15, 21, 25, 27, 35, 91, 143, 221, 341,
            561, 1105, 1729, 2465, 2821, 6601
        ]

        trials_per_n = 50
        fermat_fp_rates = []
        mr_fp_rates = []

        for k in k_values:
            fermat_false_primes = 0
            mr_false_primes = 0
            total = 0

            for n in composites:
                for t in range(trials_per_n):
                    total += 1
                    seed = 1000 + 97 * t + n
                    if fermat_primality(n, k=k, seed=seed):
                        fermat_false_primes += 1
                    if miller_rabin_primality(n, k=k, seed=seed):
                        mr_false_primes += 1

            fermat_fp = fermat_false_primes / total
            mr_fp = mr_false_primes / total
            fermat_fp_rates.append(fermat_fp)
            mr_fp_rates.append(mr_fp)

            _write_row(w, "primality_fp_rate", "", f"k={k}", "", "", "", "", f"FermatFP={fermat_fp:.6f}", f"MRFP={mr_fp:.6f}")

            print(f"[Primality FP] k={k:2d} | Fermat FP={fermat_fp:.4f} | MR FP={mr_fp:.4f} | trials={total}")

        plt.figure()
        plt.plot(k_values, fermat_fp_rates, marker="o", label="Fermat false-positive rate")
        plt.plot(k_values, mr_fp_rates, marker="o", label="Miller–Rabin false-positive rate")
        plt.xlabel("k (iterations)")
        plt.ylabel("False positive rate on composites")
        plt.title("Monte Carlo primality: false positive rate vs k")
        plt.legend()
        fig_prime_acc = os.path.join(out_dir, "primality_accuracy.png")
        plt.savefig(fig_prime_acc, dpi=200, bbox_inches="tight")
        print(f"Saved plot: {fig_prime_acc}")

        # Speed comparison vs deterministic trial division
        large_nums = [
            1_000_003,
            1_000_000_007,
            1_000_000_009,
            1_000_000_000,
            999_999_937,
        ]
        speed_repeats = 5
        k_for_speed = 10

        det_times, fermat_times, mr_times = [], [], []

        for n in large_nums:
            dt = stats.mean(_time_one(is_prime_trial_division, n) for _ in range(speed_repeats))
            ft = stats.mean(_time_one(lambda x: fermat_primality(x, k=k_for_speed, seed=123), n) for _ in range(speed_repeats))
            mt = stats.mean(_time_one(lambda x: miller_rabin_primality(x, k=k_for_speed, seed=123), n) for _ in range(speed_repeats))

            det_times.append(dt)
            fermat_times.append(ft)
            mr_times.append(mt)

            _write_row(w, "primality_speed_fermat", n, f"k={k_for_speed}", dt, 0.0, ft, 0.0)
            _write_row(w, "primality_speed_mr", n, f"k={k_for_speed}", dt, 0.0, mt, 0.0)

            print(f"[Primality speed] n={n:,} | det={dt:.6f}s | fermat={ft:.6f}s | mr={mt:.6f}s")

        x = list(range(len(large_nums)))
        plt.figure()
        plt.plot(x, det_times, marker="o", label="Deterministic trial division")
        plt.plot(x, fermat_times, marker="o", label=f"Fermat (k={k_for_speed})")
        plt.plot(x, mr_times, marker="o", label=f"Miller–Rabin (k={k_for_speed})")
        plt.xticks(x, [f"{n:,}" for n in large_nums], rotation=25, ha="right")
        plt.ylabel("Mean runtime (seconds)")
        plt.title("Primality test runtime comparison")
        plt.legend()
        fig_prime_speed = os.path.join(out_dir, "primality_speed.png")
        plt.savefig(fig_prime_speed, dpi=200, bbox_inches="tight")
        print(f"Saved plot: {fig_prime_speed}")

        # ============================================================
        # Part 4: Bloom Filter — false positive rate vs load
        # ============================================================
        m_bits = 100_000
        k_hashes = 7
        bf = BloomFilter(m_bits=m_bits, k_hashes=k_hashes)

        insert_counts = [1000, 3000, 10_000, 30_000, 50_000]
        query_trials = 10_000

        fp_rates_emp = []
        fp_rates_theory = []

        inserted = set()
        next_id = 0

        for n_insert in insert_counts:
            while len(inserted) < n_insert:
                item = f"item_{next_id}"
                next_id += 1
                inserted.add(item)
                bf.add(item)

            false_pos = 0
            for j in range(query_trials):
                q = f"query_{n_insert}_{j}"
                if bf.check(q):
                    false_pos += 1

            fp_emp = false_pos / query_trials
            fp_th = bf.estimated_false_positive_rate(n_inserted=n_insert)

            fp_rates_emp.append(fp_emp)
            fp_rates_theory.append(fp_th)

            load_factor = n_insert / m_bits
            _write_row(
                w,
                "bloom_fp_rate",
                n_insert,
                f"m={m_bits},k={k_hashes}",
                "", "", "", "",
                f"load={load_factor:.4f}",
                f"emp={fp_emp:.6f},theory={fp_th:.6f}",
            )

            print(f"[Bloom] n={n_insert:6d} load={load_factor:.4f} | empFP={fp_emp:.4f} theoryFP={fp_th:.4f}")

        plt.figure()
        plt.plot(insert_counts, fp_rates_emp, marker="o", label="Empirical FP rate")
        plt.plot(insert_counts, fp_rates_theory, marker="o", label="Theoretical approx FP rate")
        plt.xscale("log")
        plt.xlabel("Items inserted (n)")
        plt.ylabel("False positive rate")
        plt.title(f"Bloom filter FP rate vs load (m={m_bits} bits, k={k_hashes})")
        plt.legend()
        fig_bloom = os.path.join(out_dir, "bloom_filter_fp_rate.png")
        plt.savefig(fig_bloom, dpi=200, bbox_inches="tight")
        print(f"Saved plot: {fig_bloom}")

        # ============================================================
        # Part 5: MinHash similarity estimation (error vs k)
        # ============================================================
        A = {f"t{i}" for i in range(200)}
        B = {f"t{i}" for i in range(100, 300)}
        true_j = jaccard_similarity(A, B)

        ks = [16, 32, 64, 128, 256, 512]
        abs_errors = []

        for k in ks:
            t_j, est_j = minhash_estimate(A, B, k=k)
            err = abs(est_j - t_j)
            abs_errors.append(err)

            _write_row(w, "minhash_error", k, "A vs B", "", "", "", "", f"true={t_j:.6f}", f"est={est_j:.6f},abs_err={err:.6f}")
            print(f"[MinHash] k={k:3d} | true={t_j:.4f} est={est_j:.4f} abs_err={err:.4f}")

        plt.figure()
        plt.plot(ks, abs_errors, marker="o", label="Absolute error |est - true|")
        plt.xscale("log")
        plt.xlabel("Signature size k (log scale)")
        plt.ylabel("Absolute error")
        plt.title(f"MinHash estimation error vs k (true J={true_j:.3f})")
        plt.legend()
        fig_minhash = os.path.join(out_dir, "minhash_similarity_plot.png")
        plt.savefig(fig_minhash, dpi=200, bbox_inches="tight")
        print(f"Saved plot: {fig_minhash}")

    print(f"\nSaved summary CSV: {summary_csv}")
    print("Done.")


if __name__ == "__main__":
    main()