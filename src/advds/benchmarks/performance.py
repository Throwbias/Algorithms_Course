import csv
import random
import time
from pathlib import Path

import matplotlib.pyplot as plt

from advds.trees.segment_tree import SegmentTree
from advds.trees.fenwick_tree import FenwickTree
from advds.trees.persistent_tree import PersistentSegmentTree
from advds.succinct.bit_vector import BitVector
from advds.succinct.wavelet_tree import WaveletTree
from advds.cache_oblivious.matrix_ops import (
    naive_multiply,
    cache_oblivious_multiply,
    naive_transpose,
    cache_oblivious_transpose,
)


RESULTS_DIR = Path(__file__).resolve().parents[3] / "results" / "week13"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)


def write_csv(filename, rows, fieldnames):
    path = RESULTS_DIR / filename
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    return path


def make_line_plot(x, y_series, xlabel, ylabel, title, filename):
    plt.figure(figsize=(8, 5))
    for label, ys in y_series.items():
        plt.plot(x, ys, marker="o", label=label)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.legend()
    plt.tight_layout()
    out = RESULTS_DIR / filename
    plt.savefig(out, dpi=150)
    plt.close()
    return out


def time_call(fn, *args, repeats=3, **kwargs):
    best = float("inf")
    result = None
    for _ in range(repeats):
        start = time.perf_counter()
        result = fn(*args, **kwargs)
        elapsed = time.perf_counter() - start
        if elapsed < best:
            best = elapsed
    return best, result


def random_array(n, low=0, high=1000):
    return [random.randint(low, high) for _ in range(n)]


def random_bits(n):
    return [random.randint(0, 1) for _ in range(n)]


def random_matrix(n, low=0, high=10):
    return [[random.randint(low, high) for _ in range(n)] for _ in range(n)]


def benchmark_segment_vs_fenwick():
    sizes = [100, 500, 1000, 2000, 5000]
    rows = []

    seg_query_times = []
    fen_query_times = []
    seg_update_times = []
    fen_update_times = []

    for n in sizes:
        arr = random_array(n)
        queries = [(random.randint(0, n - 1), random.randint(0, n - 1)) for _ in range(200)]
        queries = [(min(a, b), max(a, b)) for a, b in queries]
        updates = [(random.randint(0, n - 1), random.randint(0, 1000)) for _ in range(200)]

        seg = SegmentTree(arr)
        fen = FenwickTree(arr)
        shadow = arr[:]

        def run_seg_queries():
            total = 0
            for l, r in queries:
                total += seg.query(l, r)
            return total

        def run_fen_queries():
            total = 0
            for l, r in queries:
                total += fen.range_sum(l, r)
            return total

        def run_seg_updates():
            for idx, new_val in updates:
                try:
                    seg.update(idx, new_val)
                except AttributeError:
                    current = seg.query(idx, idx)
                    seg.range_update(idx, idx, new_val - current)

        def run_fen_updates():
            for idx, new_val in updates:
                delta = new_val - shadow[idx]
                shadow[idx] = new_val
                fen.update(idx, delta)

        seg_q_time, _ = time_call(run_seg_queries)
        fen_q_time, _ = time_call(run_fen_queries)
        seg_u_time, _ = time_call(run_seg_updates, repeats=1)
        fen_u_time, _ = time_call(run_fen_updates, repeats=1)

        seg_query_times.append(seg_q_time)
        fen_query_times.append(fen_q_time)
        seg_update_times.append(seg_u_time)
        fen_update_times.append(fen_u_time)

        rows.append({
            "input_size": n,
            "segment_query_time_sec": seg_q_time,
            "fenwick_query_time_sec": fen_q_time,
            "segment_update_time_sec": seg_u_time,
            "fenwick_update_time_sec": fen_u_time,
            "num_queries": len(queries),
            "num_updates": len(updates),
        })

    write_csv(
        "segment_vs_fenwick.csv",
        rows,
        [
            "input_size",
            "segment_query_time_sec",
            "fenwick_query_time_sec",
            "segment_update_time_sec",
            "fenwick_update_time_sec",
            "num_queries",
            "num_updates",
        ],
    )

    make_line_plot(
        sizes,
        {
            "Segment Query": seg_query_times,
            "Fenwick Query": fen_query_times,
        },
        "Input Size",
        "Time (sec)",
        "Segment Tree vs Fenwick Tree Query Performance",
        "segment_vs_fenwick_queries.png",
    )

    make_line_plot(
        sizes,
        {
            "Segment Update": seg_update_times,
            "Fenwick Update": fen_update_times,
        },
        "Input Size",
        "Time (sec)",
        "Segment Tree vs Fenwick Tree Update Performance",
        "segment_vs_fenwick_updates.png",
    )


def benchmark_persistent_overhead():
    sizes = [100, 500, 1000, 2000]
    rows = []

    build_times = []
    update_times = []

    for n in sizes:
        arr = random_array(n)
        pst_build_time, pst = time_call(PersistentSegmentTree, arr)

        updates = [(random.randint(0, n - 1), random.randint(0, 1000)) for _ in range(200)]

        def run_updates():
            current_version = 0
            for idx, val in updates:
                current_version = pst.update(current_version, idx, val)
            return current_version

        pst_update_time, latest_version = time_call(run_updates, repeats=1)

        rows.append({
            "input_size": n,
            "build_time_sec": pst_build_time,
            "update_batch_time_sec": pst_update_time,
            "num_updates": len(updates),
            "versions_created": latest_version + 1,
        })

        build_times.append(pst_build_time)
        update_times.append(pst_update_time)

    write_csv(
        "persistent_tree_overhead.csv",
        rows,
        [
            "input_size",
            "build_time_sec",
            "update_batch_time_sec",
            "num_updates",
            "versions_created",
        ],
    )

    make_line_plot(
        sizes,
        {
            "Build Time": build_times,
            "Update Batch Time": update_times,
        },
        "Input Size",
        "Time (sec)",
        "Persistent Tree Overhead",
        "persistent_tree_overhead.png",
    )


def benchmark_bitvector_rank_select():
    sizes = [1000, 5000, 10000, 20000, 50000]
    rows = []

    rank_times = []
    select_times = []

    for n in sizes:
        bits = random_bits(n)
        bv = BitVector(bits)

        rank_indices = [random.randint(0, n - 1) for _ in range(500)]
        ones_count = max(1, sum(bits))
        select_indices = [random.randint(1, ones_count) for _ in range(500)]

        def run_rank():
            total = 0
            for i in rank_indices:
                total += bv.rank1(i)
            return total

        def run_select():
            total = 0
            for k in select_indices:
                total += bv.select1(k)
            return total

        rank_time, _ = time_call(run_rank)
        select_time, _ = time_call(run_select)

        rows.append({
            "input_size": n,
            "rank_time_sec": rank_time,
            "select_time_sec": select_time,
            "ones_count": sum(bits),
            "zeros_count": n - sum(bits),
        })

        rank_times.append(rank_time)
        select_times.append(select_time)

    write_csv(
        "bitvector_rank_select.csv",
        rows,
        [
            "input_size",
            "rank_time_sec",
            "select_time_sec",
            "ones_count",
            "zeros_count",
        ],
    )

    make_line_plot(
        sizes,
        {
            "rank1": rank_times,
            "select1": select_times,
        },
        "Input Size",
        "Time (sec)",
        "BitVector Rank/Select Performance",
        "bitvector_rank_select.png",
    )


def benchmark_wavelet_tree():
    sizes = [100, 500, 1000, 2000, 5000]
    alphabet = list("ACGT")
    rows = []

    build_times = []
    query_times = []
    compression_ratios = []

    for n in sizes:
        data = [random.choice(alphabet) for _ in range(n)]

        build_time, wt = time_call(WaveletTree, data)

        freq_queries = [
            (random.choice(alphabet), min(a, b), max(a, b))
            for a, b in [
                (random.randint(0, n - 1), random.randint(0, n - 1))
                for _ in range(300)
            ]
        ]

        def run_queries():
            total = 0
            for char, l, r in freq_queries:
                total += wt.frequency(char, l, r)
            return total

        query_time, _ = time_call(run_queries)

        raw_chars = len(data)
        bitvector_bits = sum(len(node.bitvector.bits) for node in _collect_wavelet_nodes(wt))
        compression_ratio = bitvector_bits / raw_chars if raw_chars else 0.0

        rows.append({
            "input_size": n,
            "build_time_sec": build_time,
            "query_time_sec": query_time,
            "bitvector_bits": bitvector_bits,
            "raw_symbols": raw_chars,
            "compression_ratio_proxy": compression_ratio,
        })

        build_times.append(build_time)
        query_times.append(query_time)
        compression_ratios.append(compression_ratio)

    write_csv(
        "wavelet_tree.csv",
        rows,
        [
            "input_size",
            "build_time_sec",
            "query_time_sec",
            "bitvector_bits",
            "raw_symbols",
            "compression_ratio_proxy",
        ],
    )

    make_line_plot(
        sizes,
        {
            "Build Time": build_times,
            "Query Time": query_times,
        },
        "Input Size",
        "Time (sec)",
        "Wavelet Tree Build and Query Performance",
        "wavelet_tree_times.png",
    )

    make_line_plot(
        sizes,
        {
            "Compression Ratio Proxy": compression_ratios,
        },
        "Input Size",
        "Ratio",
        "Wavelet Tree Compression Ratio Proxy",
        "wavelet_tree_compression.png",
    )


def _collect_wavelet_nodes(node):
    if node is None:
        return []
    nodes = [node]
    nodes.extend(_collect_wavelet_nodes(node.left))
    nodes.extend(_collect_wavelet_nodes(node.right))
    return nodes


def benchmark_matrix_ops():
    sizes = [2, 4, 8, 16]
    rows = []

    transpose_naive_times = []
    transpose_co_times = []
    multiply_naive_times = []
    multiply_co_times = []

    for n in sizes:
        a = random_matrix(n)
        b = random_matrix(n)

        t_naive, naive_t = time_call(naive_transpose, a)
        t_co, co_t = time_call(cache_oblivious_transpose, a)
        m_naive, naive_m = time_call(naive_multiply, a, b, repeats=1)
        m_co, co_m = time_call(cache_oblivious_multiply, a, b, repeats=1)

        if naive_t != co_t:
            raise ValueError(f"Transpose mismatch at size {n}")
        if naive_m != co_m:
            raise ValueError(f"Multiply mismatch at size {n}")

        rows.append({
            "matrix_size": n,
            "naive_transpose_time_sec": t_naive,
            "cache_oblivious_transpose_time_sec": t_co,
            "naive_multiply_time_sec": m_naive,
            "cache_oblivious_multiply_time_sec": m_co,
        })

        transpose_naive_times.append(t_naive)
        transpose_co_times.append(t_co)
        multiply_naive_times.append(m_naive)
        multiply_co_times.append(m_co)

    write_csv(
        "matrix_ops.csv",
        rows,
        [
            "matrix_size",
            "naive_transpose_time_sec",
            "cache_oblivious_transpose_time_sec",
            "naive_multiply_time_sec",
            "cache_oblivious_multiply_time_sec",
        ],
    )

    make_line_plot(
        sizes,
        {
            "Naive Transpose": transpose_naive_times,
            "Cache-Oblivious Transpose": transpose_co_times,
        },
        "Matrix Size",
        "Time (sec)",
        "Matrix Transpose Performance",
        "matrix_transpose_performance.png",
    )

    make_line_plot(
        sizes,
        {
            "Naive Multiply": multiply_naive_times,
            "Cache-Oblivious Multiply": multiply_co_times,
        },
        "Matrix Size",
        "Time (sec)",
        "Matrix Multiplication Performance",
        "matrix_multiply_performance.png",
    )


def run_all_benchmarks(seed=42):
    random.seed(seed)
    benchmark_segment_vs_fenwick()
    benchmark_persistent_overhead()
    benchmark_bitvector_rank_select()
    benchmark_wavelet_tree()
    benchmark_matrix_ops()
    print(f"Benchmark results written to: {RESULTS_DIR.resolve()}")


if __name__ == "__main__":
    run_all_benchmarks()