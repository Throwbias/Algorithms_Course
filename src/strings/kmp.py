"""
Knuth-Morris-Pratt (KMP) string matching.

Implements:
- LPS / prefix-function computation
- first-match search
- all-match search

Complexity:
- preprocessing: O(m)
- search: O(n + m)
"""

from typing import List


def compute_lps(pattern: str) -> List[int]:
    """
    Compute the LPS (longest proper prefix which is also suffix) array.

    Args:
        pattern: pattern string

    Returns:
        list of LPS values
    """
    if pattern == "":
        return []

    lps = [0] * len(pattern)
    length = 0
    i = 1

    while i < len(pattern):
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1

    return lps


def kmp_search(text: str, pattern: str) -> int:
    """
    Return the index of the first match of pattern in text, or -1 if absent.

    Args:
        text: text to search
        pattern: pattern to find

    Returns:
        starting index of first match, or -1
    """
    if pattern == "":
        return 0
    if len(pattern) > len(text):
        return -1

    lps = compute_lps(pattern)
    i = 0  # index for text
    j = 0  # index for pattern

    while i < len(text):
        if text[i] == pattern[j]:
            i += 1
            j += 1

            if j == len(pattern):
                return i - j
        else:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1

    return -1


def kmp_search_all(text: str, pattern: str) -> List[int]:
    """
    Return all starting indices where pattern appears in text.

    Args:
        text: text to search
        pattern: pattern to find

    Returns:
        list of match starting indices
    """
    if pattern == "":
        return list(range(len(text) + 1))
    if len(pattern) > len(text):
        return []

    lps = compute_lps(pattern)
    matches = []

    i = 0
    j = 0

    while i < len(text):
        if text[i] == pattern[j]:
            i += 1
            j += 1

            if j == len(pattern):
                matches.append(i - j)
                j = lps[j - 1]
        else:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1

    return matches