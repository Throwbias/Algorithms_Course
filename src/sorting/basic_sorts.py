from typing import List

def bubble_sort(arr: List[int]) -> List[int]:
    """
    Optimized Bubble Sort.
    Returns a new sorted list without modifying the input.
    """
    a = arr.copy()
    n = len(a)
    
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
                swapped = True
        if not swapped:
            break
    return a


def selection_sort(arr: List[int]) -> List[int]:
    """
    Selection Sort.
    Returns a new sorted list without modifying the input.
    """
    a = arr.copy()
    n = len(a)
    
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if a[j] < a[min_idx]:
                min_idx = j
        a[i], a[min_idx] = a[min_idx], a[i]
    return a


def insertion_sort(arr: List[int]) -> List[int]:
    """
    Insertion Sort.
    Returns a new sorted list without modifying the input.
    """
    a = arr.copy()
    for i in range(1, len(a)):
        key = a[i]
        j = i - 1
        while j >= 0 and key < a[j]:
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = key
    return a
