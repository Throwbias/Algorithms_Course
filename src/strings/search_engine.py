"""
Unified String Search Engine.

Supports:
- KMP
- Rabin-Karp
- Suffix Array
- Compressed Suffix Tree
"""

import time
from typing import Dict, Any, List, Optional

from src.strings.kmp import kmp_search_all
from src.strings.rabin_karp import rabin_karp_search_all
from src.strings.suffix_array import build_suffix_array, build_lcp_array, suffix_array_search
from src.strings.suffix_tree import CompressedSuffixTree


class StringSearchEngine:
    def __init__(self, text: str):
        self.text = text
        self._suffix_array: Optional[List[int]] = None
        self._lcp_array: Optional[List[int]] = None
        self._sa_build_time: Optional[float] = None

        self._suffix_tree: Optional[CompressedSuffixTree] = None
        self._tree_build_time: Optional[float] = None

    def _ensure_suffix_array(self) -> None:
        if self._suffix_array is None:
            start = time.perf_counter()
            self._suffix_array = build_suffix_array(self.text)
            self._lcp_array = build_lcp_array(self.text, self._suffix_array)
            self._sa_build_time = time.perf_counter() - start

    def _ensure_suffix_tree(self) -> None:
        if self._suffix_tree is None:
            start = time.perf_counter()
            self._suffix_tree = CompressedSuffixTree(self.text)
            self._tree_build_time = time.perf_counter() - start

    def find(self, pattern: str, method: str = "kmp") -> Dict[str, Any]:
        method = method.lower()
        preprocessing_time = 0.0

        if method == "kmp":
            start = time.perf_counter()
            matches = kmp_search_all(self.text, pattern)
            search_time = time.perf_counter() - start

        elif method == "rk":
            start = time.perf_counter()
            matches = rabin_karp_search_all(self.text, pattern)
            search_time = time.perf_counter() - start

        elif method == "sa":
            self._ensure_suffix_array()
            preprocessing_time = self._sa_build_time or 0.0
            start = time.perf_counter()
            matches = suffix_array_search(self.text, pattern, self._suffix_array)
            search_time = time.perf_counter() - start

        elif method == "tree":
            self._ensure_suffix_tree()
            preprocessing_time = self._tree_build_time or 0.0
            start = time.perf_counter()
            matches = self._suffix_tree.search(pattern)
            search_time = time.perf_counter() - start

        else:
            raise ValueError("method must be one of: 'kmp', 'rk', 'sa', 'tree'")

        return {
            "method": method,
            "pattern": pattern,
            "matches": matches,
            "match_count": len(matches),
            "search_time_sec": search_time,
            "preprocessing_time_sec": preprocessing_time,
            "recommendation": self.recommend(method),
        }

    def recommend(self, method: Optional[str] = None) -> str:
        recommendations = {
            "kmp": "KMP is a good choice for deterministic linear-time single-pattern scanning.",
            "rk": "Rabin-Karp is useful for rolling-hash based matching and large batch-style comparisons.",
            "sa": "Suffix Arrays are best when the same text will be queried repeatedly after preprocessing.",
            "tree": "Suffix Trees support very fast substring queries after preprocessing, at the cost of more memory and construction complexity.",
        }

        if method is not None:
            method = method.lower()
            if method not in recommendations:
                raise ValueError("method must be one of: 'kmp', 'rk', 'sa', 'tree'")
            return recommendations[method]

        return (
            "Use KMP for reliable one-off exact matching, Rabin-Karp for hash-based search, "
            "Suffix Arrays for repeated indexed queries, and Suffix Trees for fast substring lookup "
            "when preprocessing cost is acceptable."
        )

    @property
    def suffix_array(self) -> Optional[List[int]]:
        return self._suffix_array

    @property
    def lcp_array(self) -> Optional[List[int]]:
        return self._lcp_array

    @property
    def suffix_tree(self) -> Optional[CompressedSuffixTree]:
        return self._suffix_tree