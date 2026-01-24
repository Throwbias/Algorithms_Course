import random
from typing import List

def quick_sort(arr: List[int], low: int = None, high: int = None, threshold: int = 10) -> List[int]:
    """
    QuickSort algorithm with randomized pivot and insertion sort optimization.

    Args:
        arr (List[int]): The input list to sort.
        low (int): Starting index (default None, sets to 0).
        high (int): Ending index (default None, sets to len(arr)-1).
        threshold (int): Switch to insertion sort for subarrays smaller than this.

    Returns:
        List[int]: Sorted list (non-destructive).
    """
    if low is None or high is None:
        arr = arr.copy()  # non-destructive
        low = 0
        high = len(arr) - 1

    def insertion_sort(sub_arr: List[int], left: int, right: int):
        for i in range(left + 1, right + 1):
            key = sub_arr[i]
            j = i - 1
            while j >= left and sub_arr[j] > key:
                sub_arr[j + 1] = sub_arr[j]
                j -= 1
            sub_arr[j + 1] = key

    def partition(l: int, h: int) -> int:
        pivot_index = random.randint(l, h)
        arr[h], arr[pivot_index] = arr[pivot_index], arr[h]  # move pivot to end
        pivot = arr[h]
        i = l - 1
        for j in range(l, h):
            if arr[j] <= pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
        arr[i + 1], arr[h] = arr[h], arr[i + 1]
        return i + 1

    def _quick_sort(l: int, h: int):
        if l < h:
            if h - l + 1 <= threshold:
                insertion_sort(arr, l, h)
            else:
                pi = partition(l, h)
                _quick_sort(l, pi - 1)
                _quick_sort(pi + 1, h)

    _quick_sort(low, high)
    return arr
