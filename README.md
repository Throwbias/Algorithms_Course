# Algorithms Course — Core Techniques

This repository contains implementations, benchmarks, and technical analysis for core algorithmic design techniques including deterministic algorithms, dynamic programming, graph algorithms, and randomized computation.

---

# Week 7 — Randomized Algorithms

Week 7 focuses on probabilistic algorithm design and randomized data structures.  
The goal of this module was to explore how randomness improves robustness, scalability, and expected performance while maintaining bounded probabilistic guarantees.

## Implemented Algorithms

### Las Vegas Algorithms (Always Correct, Random Runtime)
- Randomized QuickSort
- Randomized QuickSelect

### Monte Carlo Algorithms (Probabilistic Accuracy)
- Fermat Primality Test
- Miller–Rabin Primality Test

### Probabilistic Data Structures
- Bloom Filter (probabilistic membership testing)
- MinHash (Jaccard similarity estimation)

---

## Benchmark Execution

All Week 7 results are generated using:

```bash
python -m benchmarks.week7_randomized_benchmark
```

All outputs are saved in:

```
benchmarks/results/
```

### Generated Visualizations

- quicksort_comparison.png  
- quicksort_comparison_sorted.png  
- selection_runtime.png  
- primality_accuracy.png  
- primality_speed.png  
- bloom_filter_fp_rate.png  
- minhash_similarity_plot.png  
- summary_table.csv  

These plots validate theoretical expectations and empirically demonstrate performance trade-offs between deterministic and probabilistic techniques.

---

## Testing

Run all randomized module tests:

```bash
pytest tests/randomized -v
```

All components are fully tested and reproducible.

---

## Key Concepts Demonstrated

- Las Vegas vs Monte Carlo algorithms  
- Expected O(n log n) vs adversarial worst-case behavior  
- Probabilistic error bounds  
- False positive rates and load factors  
- Runtime variance analysis  
- Similarity estimation using randomized hashing  
- Empirical validation of theoretical complexity  

---

## Repository Structure

```
src/
    sorting/
    randomized/
    dp/
    graphs/
    structures/

benchmarks/
    week7_randomized_benchmark.py
    results/

tests/
    randomized/

reports/
    Week7_Report.md
```

---

# GitHub

Full project is hosted here:  
https://github.com/Throwbias/Algorithms_Course.git  

Includes **all source code, tests, benchmarking results, and plots** for verification.

---

## Author

Aaron Tobias  
Master’s Level Algorithms Coursework  
Algorithms and Systems Analysis