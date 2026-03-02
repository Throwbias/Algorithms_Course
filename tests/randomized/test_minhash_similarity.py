from src.randomized.minhash_similarity import (
    jaccard_similarity,
    minhash_signature,
    estimate_jaccard_from_signatures,
    minhash_estimate,
)


def test_jaccard_basic():
    a = {"a", "b", "c"}
    b = {"b", "c", "d"}
    assert jaccard_similarity(a, b) == 2 / 4


def test_signature_length():
    a = {"a", "b", "c"}
    sig = minhash_signature(a, k=32)
    assert len(sig) == 32


def test_estimate_bounds():
    a = {"a", "b", "c", "d", "e"}
    b = {"c", "d", "e", "f", "g"}
    true_j, est_j = minhash_estimate(a, b, k=128)
    assert 0.0 <= est_j <= 1.0
    assert 0.0 <= true_j <= 1.0


def test_estimate_identical_sets():
    a = {"x", "y", "z"}
    true_j, est_j = minhash_estimate(a, a, k=64)
    assert true_j == 1.0
    assert est_j == 1.0


def test_estimator_converges_with_k():
    # not strict convergence, but error should usually be smaller for larger k
    a = {f"t{i}" for i in range(100)}
    b = {f"t{i}" for i in range(50, 150)}

    true_j, est16 = minhash_estimate(a, b, k=16)
    _, est256 = minhash_estimate(a, b, k=256)

    err16 = abs(est16 - true_j)
    err256 = abs(est256 - true_j)

    # allow some noise, but generally larger k should not be worse by a lot
    assert err256 <= err16 + 0.25