from __future__ import annotations

import hashlib
from typing import Iterable, List, Set, Tuple


def jaccard_similarity(a: Set[str], b: Set[str]) -> float:
    if not a and not b:
        return 1.0
    inter = len(a & b)
    union = len(a | b)
    return inter / union if union else 1.0


def _hash_token(token: str, salt: int) -> int:
    # stable across runs
    h = hashlib.blake2b(digest_size=8)
    h.update(salt.to_bytes(4, "little", signed=False))
    h.update(token.encode("utf-8"))
    return int.from_bytes(h.digest(), "big")


def minhash_signature(tokens: Iterable[str], k: int) -> List[int]:
    """
    Compute MinHash signature (length k) for a token set.
    signature[i] = min hash value under hash function i
    """
    tok_list = list(tokens)
    if k <= 0:
        raise ValueError("k must be > 0")
    if not tok_list:
        # empty set: signature all max values
        return [2**64 - 1] * k

    sig = []
    for i in range(k):
        m = None
        for t in tok_list:
            hv = _hash_token(t, i + 1)
            if m is None or hv < m:
                m = hv
        sig.append(m if m is not None else 2**64 - 1)
    return sig


def estimate_jaccard_from_signatures(sig_a: List[int], sig_b: List[int]) -> float:
    if len(sig_a) != len(sig_b):
        raise ValueError("Signature lengths must match")
    if not sig_a:
        return 1.0
    matches = sum(1 for x, y in zip(sig_a, sig_b) if x == y)
    return matches / len(sig_a)


def minhash_estimate(a: Set[str], b: Set[str], k: int) -> Tuple[float, float]:
    """
    Returns (true_jaccard, estimated_jaccard)
    """
    true_j = jaccard_similarity(a, b)
    sig_a = minhash_signature(a, k)
    sig_b = minhash_signature(b, k)
    est_j = estimate_jaccard_from_signatures(sig_a, sig_b)
    return true_j, est_j