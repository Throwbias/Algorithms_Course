import random
from typing import List, TypeVar

T = TypeVar("T")


def quick_sort(arr: List[T]) -> List[T]:
    """
    Sorts a list using optimized QuickSort.

    Features:
    - Randomized pivot selection
    - Three-way partitioning (handles duplicates efficiently)
    - Insertion sort for small subarrays
    - Returns a new sorted list (does not modify input)

    Average Time: O(n log n)
    Worst Time: O(n^2) (rare due to randomization)
    Space: O(log n) recursion stack
    """
    if len(arr) <= 1:
        return arr.copy()

    data = arr.copy()
    _quick_sort(data, 0, len(data) - 1)
    return data


def _quick_sort(arr: List[T], low: int, high: int) -> None:
    if high <= low:
        return

    # Insertion sort cutoff
    if high - low <= 10:
        _insertion_sort(arr, low, high)
        return

    lt, gt = _partition_3way(arr, low, high)
    _quick_sort(arr, low, lt - 1)
    _quick_sort(arr, gt + 1, high)


def _partition_3way(arr: List[T], low: int, high: int):
    pivot_index = random.randint(low, high)
    pivot = arr[pivot_index]
    arr[low], arr[pivot_index] = arr[pivot_index], arr[low]

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
