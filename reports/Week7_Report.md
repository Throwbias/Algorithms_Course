# Week 7 — Randomized Algorithms and Probabilistic Analysis

## Executive Summary

This project explored the transition from deterministic algorithm design to probabilistic computation. While deterministic algorithms provide fixed guarantees, randomized algorithms often achieve superior practical performance by replacing worst-case determinism with high-probability efficiency. Across QuickSort, QuickSelect, primality testing, Bloom filters, and MinHash similarity estimation, we evaluated how randomness improves robustness, scalability, and computational efficiency while introducing bounded probabilistic error.

Empirical results demonstrate that randomized methods preserve correctness (Las Vegas algorithms) or achieve controllable error bounds (Monte Carlo algorithms) while significantly improving expected performance. These techniques underpin modern systems in cryptography, distributed computing, web search, and large-scale data processing.

---

## Methodology

All experiments were conducted in Python using reproducible random seeding where appropriate. Benchmarks were executed using multiple trials to measure:

- Mean runtime  
- Runtime variance  
- False positive rates  
- Estimation error  
- Recursion depth (for QuickSelect)  

Log–log plots were used for scalability analysis where appropriate. Results were exported to `benchmarks/results/` and summarized in `summary_table.csv`.

---

# Part 1 — Randomized QuickSort (Las Vegas Algorithm)

## Objective  
Compare deterministic QuickSort (fixed pivot) against randomized QuickSort.

## Findings

1. **Random input performance**
   - Both implementations scale approximately O(n log n).
   - Empirical comparison counts align with theoretical n log n behavior.
   - Runtime variance is present in the randomized version but remains tightly bounded.

2. **Sorted (adversarial) input**
   - Deterministic QuickSort degrades significantly.
   - Randomized QuickSort remains stable.

This clearly demonstrates the power of random pivot selection: it prevents adversarial inputs from consistently triggering worst-case O(n²) behavior.

## Expected vs Empirical Comparisons

Empirical comparison counts scale proportionally to n log₂ n, confirming theoretical expectations. The observed ratio remained within a small constant factor of the theoretical baseline.

## Interpretation

Randomized QuickSort is a **Las Vegas algorithm**:
- Always correct.
- Runtime is probabilistic.
- Worst case exists but is statistically rare.

Randomization transforms worst-case vulnerability into high-probability robustness.

---

# Part 2 — Randomized Selection (QuickSelect)

## Objective  
Find the kth smallest element in expected O(n) time.

## Results

- Randomized QuickSelect scales approximately linearly.
- Deterministic baseline (`sorted()[k]`) scales O(n log n).
- Average recursion depth grows slowly with n.
- Runtime variance is minimal relative to array size.

For median selection, the randomized algorithm consistently outperformed sorting-based selection.

## Interpretation

QuickSelect is another **Las Vegas algorithm**:
- Always returns the correct kth element.
- Expected O(n) performance.
- Avoids full sorting overhead.

This demonstrates how randomization improves efficiency when full ordering is unnecessary.

---

# Part 3 — Monte Carlo Primality Testing

## Algorithms Implemented

- Fermat primality test  
- Miller–Rabin primality test  
- Deterministic trial division baseline  

## Accuracy Results

False positive rates were measured across k = 5, 10, 20.

- Fermat test exhibited false positives on Carmichael numbers.
- Miller–Rabin’s false positive rate dropped rapidly with increasing k.
- Empirical results aligned with theoretical bound:  
  Error ≤ (1/4)^k for Miller–Rabin.

## Speed Results

For large numbers (> 10⁶):

- Deterministic trial division was significantly slower.
- Miller–Rabin was orders of magnitude faster.
- Fermat was fast but less reliable.

## Interpretation

These are **Monte Carlo algorithms**:
- Runtime deterministic.
- Accuracy probabilistic.
- Error probability decreases exponentially with k.

In cryptographic contexts, Miller–Rabin provides practical certainty with dramatically improved speed.

---

# Part 4 — Bloom Filter

## Objective  
Implement probabilistic membership testing with controlled false positives.

## Results

- Empirical false positive rates closely matched theoretical approximation:
  
  p ≈ (1 − e^(−kn/m))^k

- As load factor (n/m) increased:
  - False positive rate increased.
  - Memory efficiency remained constant.

## Interpretation

Bloom filters trade absolute certainty for:

- O(1) membership checks  
- Dramatically reduced memory footprint  
- Controlled false positive probability  

They are widely used in:

- Databases
- Distributed caches
- Networking
- Blockchain systems

This is a clear example of probabilistic data structures outperforming deterministic sets under memory constraints.

---

# Part 5 — MinHash Similarity Estimation

## Objective  
Estimate Jaccard similarity using randomized hashing.

## Results

- Absolute error decreased as signature size k increased.
- Error roughly followed expected variance reduction behavior.
- Larger k → lower estimation error.

## Interpretation

MinHash demonstrates:

- Controlled approximation
- Sublinear storage relative to raw sets
- Scalable similarity estimation

Applications include:

- Web document deduplication
- Plagiarism detection
- Large-scale clustering

Randomization enables scalable similarity comparison without explicit set intersection.

---

# Las Vegas vs Monte Carlo — A Practical Comparison

| Property | Las Vegas | Monte Carlo |
|-----------|------------|--------------|
| Correctness | Always correct | Probabilistic |
| Runtime | Probabilistic | Deterministic |
| Examples | QuickSort, QuickSelect | Miller–Rabin, Bloom filter |
| Error | None | Controlled probability |

Las Vegas algorithms trade runtime certainty for correctness.  
Monte Carlo algorithms trade correctness certainty for speed and scalability.

---

# Trade-Off Analysis

## Deterministic Guarantees
- Predictable
- Vulnerable to adversarial inputs
- Often slower at scale

## Randomized Algorithms
- High-probability efficiency
- Robust to input manipulation
- Controlled probabilistic error

Modern computing systems overwhelmingly favor randomized techniques when:

- Data is massive
- Perfect certainty is unnecessary
- Adversarial inputs are possible
- Speed is critical

---

# Conclusion

This project illustrates a fundamental shift in algorithmic thinking:

Deterministic algorithms guarantee exact behavior, but randomness provides robustness, scalability, and expected efficiency.

Randomization transforms worst-case scenarios into statistical outliers. It replaces rigid guarantees with high-confidence performance. In practice, this approach underlies cryptographic systems, distributed databases, streaming analytics, machine learning, and web-scale similarity detection.

Week 7 marks a transition from classical algorithm design toward modern probabilistic computation — where correctness, speed, and confidence are balanced strategically rather than absolutely.

# GitHub
Full project is hosted here: https://github.com/Throwbias/Algorithms_Course.git  
Includes **all source code, tests, benchmarking results, and plots** for verification.