# Week 2 Project Report

**Course:** CSC5302 – Operating Systems  
**Student:** Aaron Tobias  
**Professor:** Ostrowski  
**Date:** 2026-01-24

---

## 1. Overview

This report documents the Week 2 project for the Algorithms course. It includes objectives, implementation details, performance analysis, testing, and reflections. This week’s work builds upon Week 1, extending previous implementations and benchmarks.  

> Reference: Week 1 project located in `Week1_Report.md` and benchmarks in `benchmarks/week1_benchmark.py`.

---

## 2. Objectives

- Extend the sorting algorithm implementations from Week 1.  
- Implement performance benchmarking for new algorithms in `benchmarks/week2_performance.py`.  
- Compare Week 2 results to Week 1 performance to identify improvements.  

---

## 3. Implementation

### 3.1 File Structure

├─ benchmarks/
│ ├─ results/
│ ├─ week1_benchmark.py
│ └─ week2_performance.py
├─ scripts/
│ └─ environment_check.py
├─ src/
│ ├─ sorting/
│ └─ init.py
├─ tests/
│ ├─ test_basic_sorts.py
│ ├─ test_merge_sort.py
│ └─ test_quick_sort.py
├─ Week1_Report.md
├─ Week2_Report.md
├─ README.md
├─ requirements.txt
└─ pytest.ini

### 3.2 Key Components

- **`week2_performance.py`**: Implements benchmark tests for Week 2 algorithms.  
- **`src/sorting/`**: Contains updated or new sorting algorithm implementations.  
- **`tests/`**: Unit tests adapted to verify the new implementations.  

### 3.3 Code Highlights

```python
# Example: benchmarking function from week2_performance.py
from time import perf_counter
from src.sorting.quick_sort import quick_sort

def benchmark_sort(array):
    start = perf_counter()
    quick_sort(array)
    end = perf_counter()
    return end - start

sample_array = [5, 2, 9, 1, 5, 6]
print(f"Quick Sort Time: {benchmark_sort(sample_array)} seconds")
4. Testing

Unit tests: All Week 2 sorting algorithms are tested with pytest using the existing tests/ directory.

Benchmark verification: Results from week2_performance.py are compared with Week 1 benchmarks to ensure correctness and track performance changes.

5. Observations & Challenges

Observation 1: Some sorting implementations were optimized for larger datasets, showing noticeable performance improvement over Week 1.

Challenge 1: Ensuring that benchmarks ran consistently across different dataset sizes required careful array generation and timing code.

6. Reflections

Week 2 reinforced the importance of measuring performance and not just correctness. By comparing results to Week 1 benchmarks, I gained insight into how algorithmic improvements translate to real-world runtime efficiency. Maintaining a consistent project structure (src, tests, benchmarks, reports) continues to be critical for clarity and reproducibility.

7. References

Week 1 Report: Week1_Report.md

Benchmarks: benchmarks/week1_benchmark.py, benchmarks/week2_performance.py

Course Textbook: Operating System Concepts, 10th Edition

 8. GitHub Repository

Full project is hosted here: https://github.com/Throwbias/Algorithms_Course.git  
Includes **all source code, tests, benchmarking results, and plots** for verification.

