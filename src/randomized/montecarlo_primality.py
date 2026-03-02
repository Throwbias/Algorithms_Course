from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Tuple
import random


@dataclass
class PrimalityStats:
    rounds: int = 0
    bases_tested: int = 0


def is_prime_deterministic(n: int) -> bool:
    """
    Deterministic trial division (baseline).
    Good for comparison; too slow for huge n but fine for n ~ 1e6..1e8 in benchmarks.
    """
    if n < 2:
        return False
    if n in (2, 3):
        return True
    if n % 2 == 0:
        return False
    i = 3
    # i*i <= n avoids floating point sqrt
    while i * i <= n:
        if n % i == 0:
            return False
        i += 2
    return True


def fermat_primality(n: int, k: int = 10, *, seed: Optional[int] = None, stats: Optional[PrimalityStats] = None) -> bool:
    """
    Fermat primality test (Monte Carlo).
    Returns True => "probably prime"
    Returns False => "composite" (definitely composite)

    Error behavior:
      - Can be fooled by Carmichael numbers.
      - For non-Carmichael composites, probability of false prime drops with k.
    """
    if stats is None:
        stats = PrimalityStats()
    stats.rounds += k

    if n < 2:
        return False
    if n in (2, 3):
        return True
    if n % 2 == 0:
        return False

    rng = random.Random(seed) if seed is not None else random

    for _ in range(k):
        # choose base a in [2, n-2]
        a = rng.randrange(2, n - 1)
        stats.bases_tested += 1
        if pow(a, n - 1, n) != 1:
            return False
    return True


def miller_rabin_primality(
    n: int, k: int = 10, *, seed: Optional[int] = None, stats: Optional[PrimalityStats] = None
) -> bool:
    """
    Miller–Rabin primality test (Monte Carlo).
    Returns True => "probably prime"
    Returns False => "composite"

    Error bound: for odd composite n, false prime probability <= (1/4)^k.
    """
    if stats is None:
        stats = PrimalityStats()
    stats.rounds += k

    if n < 2:
        return False
    if n in (2, 3):
        return True
    if n % 2 == 0:
        return False

    # write n-1 = d * 2^s with d odd
    d = n - 1
    s = 0
    while d % 2 == 0:
        d //= 2
        s += 1

    rng = random.Random(seed) if seed is not None else random

    for _ in range(k):
        a = rng.randrange(2, n - 1)
        stats.bases_tested += 1

        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue

        witness_found = True
        for _r in range(s - 1):
            x = (x * x) % n
            if x == n - 1:
                witness_found = False
                break

        if witness_found:
            return False

    return True


def classify_primality(n: int, k: int = 10, *, seed: Optional[int] = None) -> Tuple[bool, bool]:
    """
    Convenience helper: returns (fermat_probably_prime, miller_rabin_probably_prime)
    """
    return fermat_primality(n, k=k, seed=seed), miller_rabin_primality(n, k=k, seed=seed)