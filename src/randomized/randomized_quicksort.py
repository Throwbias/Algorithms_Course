from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional, TypeVar
import random

T = TypeVar("T")


@dataclass
class QuickSortStats:
    comparisons: int = 0
    partitions: int = 0


def randomized_quicksort(
    arr: List[T],
    *,
    seed: Optional[int] = None,
    stats: Optional[QuickSortStats] = None,
) -> List[T]:
    """
    Randomized QuickSort (Las Vegas):
    - Always returns a correct sorted list
    - Expected O(n log n), worst-case O(n^2) with very low probability
    - Returns a NEW list (does not modify input)
    - Optional: seed for reproducibility
    - Optional: stats collection (comparisons/partitions)

    Note: This version uses Lomuto partition (simple + good for analysis).
    """
    rng = random.Random(seed) if seed is not None else random
    data = arr.copy()
    if stats is None:
        stats = QuickSortStats()

    _rqsort_inplace(data, 0, len(data) - 1, rng, stats)
    return data


def _rqsort_inplace(a: List[T], lo: int, hi: int, rng, stats: QuickSortStats) -> None:
    if lo >= hi:
        return
    p = _partition_lomuto_random_pivot(a, lo, hi, rng, stats)
    _rqsort_inplace(a, lo, p - 1, rng, stats)
    _rqsort_inplace(a, p + 1, hi, rng, stats)


def _partition_lomuto_random_pivot(a: List[T], lo: int, hi: int, rng, stats: QuickSortStats) -> int:
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