from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional, TypeVar
import random

T = TypeVar("T")


@dataclass
class QuickSelectStats:
    partitions: int = 0
    comparisons: int = 0
    max_depth: int = 0


def randomized_selection(
    arr: List[T],
    k: int,
    *,
    seed: Optional[int] = None,
    stats: Optional[QuickSelectStats] = None,
) -> T:
    """
    Randomized QuickSelect (Las Vegas):
    - Returns the kth smallest element (0-indexed)
    - Expected O(n), worst-case O(n^2) with low probability
    - Does NOT mutate input (works on a copy)
    - Optional seed for reproducibility
    - Optional stats for partitions/comparisons/max recursion depth

    Raises:
        ValueError if k is out of bounds
    """
    if k < 0 or k >= len(arr):
        raise ValueError("k out of bounds")

    rng = random.Random(seed) if seed is not None else random
    data = arr.copy()
    if stats is None:
        stats = QuickSelectStats()

    return _quickselect(data, 0, len(data) - 1, k, rng, stats, depth=1)


def _quickselect(a: List[T], lo: int, hi: int, k: int, rng, stats: QuickSelectStats, depth: int) -> T:
    stats.max_depth = max(stats.max_depth, depth)

    if lo == hi:
        return a[lo]

    p = _partition_lomuto_random_pivot(a, lo, hi, rng, stats)

    if k == p:
        return a[p]
    elif k < p:
        return _quickselect(a, lo, p - 1, k, rng, stats, depth + 1)
    else:
        return _quickselect(a, p + 1, hi, k, rng, stats, depth + 1)


def _partition_lomuto_random_pivot(a: List[T], lo: int, hi: int, rng, stats: QuickSelectStats) -> int:
    pivot_idx = rng.randint(lo, hi)
    a[pivot_idx], a[hi] = a[hi], a[pivot_idx]
    pivot = a[hi]

    stats.partitions += 1

    i = lo
    for j in range(lo, hi):
        stats.comparisons += 1
        if a[j] <= pivot:
            a[i], a[j] = a[j], a[i]
            i += 1

    a[i], a[hi] = a[hi], a[i]
    return i