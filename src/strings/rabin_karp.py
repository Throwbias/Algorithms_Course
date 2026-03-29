"""
Rabin-Karp string matching.

Implements:
- rolling hash helper
- single-pattern first match
- single-pattern all matches

Features:
- rolling hash updates
- explicit substring verification to handle collisions

Complexity:
- average: O(n + m)
- worst case: O(nm)
"""

from typing import List


def rolling_hash(s: str, base: int = 256, modulus: int = 101) -> int:
    """
    Compute polynomial rolling hash for a string.

    Args:
        s: input string
        base: hash base
        modulus: prime modulus

    Returns:
        hash value
    """
    h = 0
    for ch in s:
        h = (h * base + ord(ch)) % modulus
    return h


def _recompute_window_hash(
    old_hash: int,
    left_char: str,
    right_char: str,
    highest_power: int,
    base: int,
    modulus: int,
) -> int:
    """
    Update rolling hash when sliding the window by one character.
    """
    new_hash = (old_hash - ord(left_char) * highest_power) % modulus
    new_hash = (new_hash * base + ord(right_char)) % modulus
    return new_hash


def rabin_karp_search(
    text: str,
    pattern: str,
    base: int = 256,
    modulus: int = 101,
) -> int:
    """
    Return the index of the first match of pattern in text, or -1 if absent.

    Args:
        text: text to search
        pattern: pattern to find
        base: rolling hash base
        modulus: prime modulus

    Returns:
        starting index of first match, or -1
    """
    matches = rabin_karp_search_all(text, pattern, base=base, modulus=modulus)
    return matches[0] if matches else -1


def rabin_karp_search_all(
    text: str,
    pattern: str,
    base: int = 256,
    modulus: int = 101,
) -> List[int]:
    """
    Return all starting indices where pattern appears in text.

    Args:
        text: text to search
        pattern: pattern to find
        base: rolling hash base
        modulus: prime modulus

    Returns:
        list of match starting indices
    """
    n = len(text)
    m = len(pattern)

    if pattern == "":
        return list(range(n + 1))
    if m > n:
        return []

    pattern_hash = rolling_hash(pattern, base=base, modulus=modulus)
    window = text[:m]
    window_hash = rolling_hash(window, base=base, modulus=modulus)

    highest_power = pow(base, m - 1, modulus)
    matches = []

    for i in range(n - m + 1):
        if pattern_hash == window_hash:
            # Verify to prevent false positive from hash collision
            if text[i:i + m] == pattern:
                matches.append(i)

        if i < n - m:
            window_hash = _recompute_window_hash(
                old_hash=window_hash,
                left_char=text[i],
                right_char=text[i + m],
                highest_power=highest_power,
                base=base,
                modulus=modulus,
            )

    return matches