# Week 1 Technical Report – Algorithms Laboratory

**Author:** Aaron Tobias  
**GitHub Repository:** https://github.com/Throwbias/Algorithms_Course.git

---

## 1. Project Overview

This project establishes my Python algorithm laboratory, implementing foundational sorting algorithms, testing their correctness, and benchmarking their performance.

**Learning Outcomes Achieved:**

- Python development environment set up and verified
- Project structure created with scalable folders
- Three sorting algorithms implemented with type hints and documentation
- Comprehensive test suite validating correctness and edge cases
- Benchmarking framework created with CSV output and performance plots

---

## 2. Project Structure

Algorithms_Course/
├─ src/
│ ├─ init.py
│ └─ sorting/
│ ├─ init.py
│ └─ basic_sorts.py
├─ tests/
│ └─ test_basic_sorts.py
├─ benchmarks/
│ ├─ week1_benchmark.py
│ └─ results/
│ ├─ week1_results.csv
│ ├─ random_plot.png
│ ├─ sorted_plot.png
│ └─ reverse_plot.png
├─ scripts/
│ └─ environment_check.py
├─ README.md
└─ requirements.txt

---

## 3. Environment Setup

- Python version: 3.14.2  
- Virtual environment created (`venv`)  
- Required packages installed via `requirements.txt` (generated using `pip freeze > requirements.txt`)  
- `pytest` tested and all tests pass  
- Environment verification script: `python scripts/environment_check.py` ✅ passed

---

## 4. Sorting Algorithms

Implemented algorithms:

1. **Bubble Sort** (optimized)  
2. **Selection Sort**  
3. **Insertion Sort**

All include:

- Type hints
- Docstrings
- Handles edge cases (empty, single-element, duplicates)
- Non-destructive to input lists (returns new sorted list)

---

## 5. Testing

- Test file: `tests/test_basic_sorts.py`  
- Uses **pytest** with parametrization for all three algorithms  
- Tests include: empty list, single element, sorted, reverse-sorted, duplicates, and random large list  
- **All tests pass** on Python 3.14.2

---

## 6. Benchmarking Framework

- File: `benchmarks/week1_benchmark.py`  
- Benchmarks each algorithm for multiple input sizes: 100, 500, 1000, 5000  
- Tests random, sorted, and reverse-sorted inputs  
- Each input size repeated multiple times to generate average execution times  
- Outputs:
  - `benchmarks/results/week1_results.csv`  
  - Performance plots (`.png`) for each data type

**Example plot:**

![Random Data Benchmark](benchmarks/results/random_plot.png)

---

## 7. Performance Analysis Summary

- **Bubble Sort** is slowest for large inputs (O(n²))  
- **Insertion Sort** performs better on nearly sorted data  
- **Selection Sort** has consistent O(n²) behavior  
- Benchmarks verify expected theoretical performance  
- Detailed results and plots are included in `benchmarks/results/` for verification

---

## 8. GitHub Repository

Full project is hosted here: https://github.com/Throwbias/Algorithms_Course.git  
Includes **all source code, tests, benchmarking results, and plots** for verification.