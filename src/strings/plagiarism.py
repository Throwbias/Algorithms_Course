"""
Plagiarism / document similarity application.

Implements:
- longest common substring using suffix-array-style approach on combined text
- simple overlap-based similarity score using fixed-length shingles

This keeps the implementation practical and report-friendly.
"""

from typing import Dict, Any, Set


def _normalize_text(text: str) -> str:
    """
    Lowercase and normalize whitespace.
    """
    return " ".join(text.lower().split())


def longest_common_substring(text1: str, text2: str) -> str:
    """
    Compute one longest common substring between two texts using
    a dynamic programming approach.

    This is practical for moderate-sized documents and sufficient for
    a course application module.
    """
    a = _normalize_text(text1)
    b = _normalize_text(text2)

    if not a or not b:
        return ""

    dp = [0] * (len(b) + 1)
    best_len = 0
    best_end = 0

    for i in range(1, len(a) + 1):
        prev = 0
        for j in range(1, len(b) + 1):
            temp = dp[j]
            if a[i - 1] == b[j - 1]:
                dp[j] = prev + 1
                if dp[j] > best_len:
                    best_len = dp[j]
                    best_end = i
            else:
                dp[j] = 0
            prev = temp

    return a[best_end - best_len:best_end]


def _shingles(text: str, shingle_size: int = 5) -> Set[str]:
    """
    Build fixed-length token shingles.
    """
    normalized = _normalize_text(text)
    tokens = normalized.split()

    if len(tokens) < shingle_size:
        return {" ".join(tokens)} if tokens else set()

    return {
        " ".join(tokens[i:i + shingle_size])
        for i in range(len(tokens) - shingle_size + 1)
    }


def plagiarism_similarity(text1: str, text2: str, shingle_size: int = 5) -> Dict[str, Any]:
    """
    Compute a simple plagiarism-style similarity summary.

    Returns:
        similarity_score: Jaccard similarity over shingles
        longest_common_substring: longest shared substring
        shared_shingles: count of shared shingles
        total_shingles_doc1
        total_shingles_doc2
    """
    s1 = _shingles(text1, shingle_size=shingle_size)
    s2 = _shingles(text2, shingle_size=shingle_size)

    union = s1 | s2
    intersection = s1 & s2

    score = len(intersection) / len(union) if union else 1.0
    lcs = longest_common_substring(text1, text2)

    return {
        "similarity_score": score,
        "longest_common_substring": lcs,
        "shared_shingles": len(intersection),
        "total_shingles_doc1": len(s1),
        "total_shingles_doc2": len(s2),
    }