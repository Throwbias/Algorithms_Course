from src.randomized.montecarlo_primality import (
    is_prime_deterministic,
    fermat_primality,
    miller_rabin_primality,
)


def test_deterministic_small_primes_and_composites():
    primes = [2, 3, 5, 7, 11, 13, 17, 19, 23]
    comps = [1, 4, 6, 8, 9, 10, 12, 15, 21, 25]

    for p in primes:
        assert is_prime_deterministic(p) is True
    for c in comps:
        assert is_prime_deterministic(c) is False


def test_fermat_detects_simple_composites():
    # Fermat should reject these quickly
    for n in [9, 15, 21, 25, 27, 35]:
        assert fermat_primality(n, k=10, seed=1) is False


def test_miller_rabin_detects_composites():
    for n in [9, 15, 21, 25, 27, 35, 91, 221]:
        assert miller_rabin_primality(n, k=10, seed=1) is False


def test_probable_primes_are_true_primes_in_small_range():
    # For small primes, both should return True
    for p in [101, 103, 107, 109, 127, 131]:
        assert fermat_primality(p, k=10, seed=2) is True
        assert miller_rabin_primality(p, k=10, seed=2) is True


def test_miller_rabin_handles_edge_cases():
    assert miller_rabin_primality(0) is False
    assert miller_rabin_primality(1) is False
    assert miller_rabin_primality(2) is True
    assert miller_rabin_primality(3) is True
    assert miller_rabin_primality(4) is False