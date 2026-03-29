"""
Suffix Array + LCP implementation.

Includes:
- O(n log n) suffix array construction (sorted suffixes approach)
- Kasai's algorithm for LCP construction
- binary-search substring lookup over the suffix array

This is sufficient for a clean course project implementation and benchmarking.
"""

from typing import List


def build_suffix_array(text: str) -> List[int]:
    """
    Build suffix array by sorting suffix start indices.

    Args:
        text: input string

    Returns:
        list of starting indices of suffixes in lexicographic order
    """
    return sorted(range(len(text)), key=lambda i: text[i:])


def build_lcp_array(text: str, suffix_array: List[int]) -> List[int]:
    """
    Build LCP array using Kasai's algorithm.

    LCP[i] = length of longest common prefix between
             suffixes starting at suffix_array[i] and suffix_array[i-1]
    with LCP[0] = 0.

    Args:
        text: input string
        suffix_array: suffix array of text

    Returns:
        LCP array
    """
    n = len(text)
    if n == 0:
        return []

    rank = [0] * n
    for i, suffix_start in enumerate(suffix_array):
        rank[suffix_start] = i

    lcp = [0] * n
    k = 0

    for i in range(n):
        if rank[i] == 0:
            k = 0
            continue

        j = suffix_array[rank[i] - 1]

        while i + k < n and j + k < n and text[i + k] == text[j + k]:
            k += 1

        lcp[rank[i]] = k

        if k > 0:
            k -= 1

    return lcp


def suffix_array_search(text: str, pattern: str, suffix_array: List[int]) -> List[int]:
    """
    Search for all occurrences of pattern using binary search over suffix array.

    Args:
        text: input text
        pattern: pattern to search
        suffix_array: precomputed suffix array

    Returns:
        sorted list of match starting indices
    """
    if pattern == "":
        return list(range(len(text) + 1))

    n = len(suffix_array)
    m = len(pattern)

    # Find left boundary
    left = 0
    right = n
    while left < right:
        mid = (left + right) // 2
        suffix = text[suffix_array[mid]:suffix_array[mid] + m]
        if suffix < pattern:
            left = mid + 1
        else:
            right = mid

    start = left

    # Find right boundary
    left = 0
    right = n
    while left < right:
        mid = (left + right) // 2
        suffix = text[suffix_array[mid]:suffix_array[mid] + m]
        if suffix <= pattern:
            left = mid + 1
        else:
            right = mid

    end = left

    matches = [
        suffix_array[i]
        for i in range(start, end)
        if text[suffix_array[i]:suffix_array[i] + m] == pattern
    ]

    return sorted(matches)