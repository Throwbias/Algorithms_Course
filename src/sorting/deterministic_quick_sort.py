# src/sorting/deterministic_quick_sort.py

from __future__ import annotations
from typing import List, TypeVar

T = TypeVar("T")


def deterministic_quick_sort(arr: List[T]) -> List[T]:
    """
    Deterministic QuickSort baseline (fixed pivot = first element).

    Features (to match your Week 2 QuickSort for fairness):
    - Three-way partitioning (handles duplicates efficiently)
    - Insertion sort cutoff for small subarrays
    - Returns a new sorted list (does not modify input)

    Average Time: O(n log n)
    Worst Time: O(n^2) on adversarial inputs (e.g., already sorted)
    Space: O(log n) recursion stack (average)
    """
    if len(arr) <= 1:
        return arr.copy()

    data = arr.copy()
    _dqsort(data, 0, len(data) - 1)
    return data


def _dqsort(arr: List[T], low: int, high: int) -> None:
    if high <= low:
        return

    # insertion sort cutoff
    if high - low <= 10:
        _insertion_sort(arr, low, high)
        return

    lt, gt = _partition_3way_first_pivot(arr, low, high)
    _dqsort(arr, low, lt - 1)
    _dqsort(arr, gt + 1, high)


def _partition_3way_first_pivot(arr: List[T], low: int, high: int):
    pivot = arr[low]
    lt = low
    i = low + 1
    gt = high

    while i <= gt:
        if arr[i] < pivot:
            arr[lt], arr[i] = arr[i], arr[lt]
            lt += 1
            i += 1
        elif arr[i] > pivot:
            arr[i], arr[gt] = arr[gt], arr[i]
            gt -= 1
        else:
            i += 1

    return lt, gt


def _insertion_sort(arr: List[T], low: int, high: int) -> None:
    for i in range(low + 1, high + 1):
        key = arr[i]
        j = i - 1
        while j >= low and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key