## Week 8 — Computational Complexity and Approximation Algorithms

This module explores the theoretical limits of computation and the behavior of algorithms for NP and NP-complete problems. The goal of this project is to demonstrate how algorithm designers handle problems that may not have efficient exact solutions by using reductions, heuristics, and approximation algorithms.

### Implemented Algorithms

**Exact Exponential Algorithms**

* Subset Sum — Backtracking implementation illustrating exponential growth
* SAT Solver — Depth-first search backtracking solver for small CNF instances

**Approximation / Heuristic Algorithms**

* Vertex Cover — 2-Approximation algorithm using greedy edge selection
* Traveling Salesman Problem (TSP) — Nearest Neighbor heuristic

**Complexity Demonstration**

* Example reduction from **3-SAT to Vertex Cover** illustrating how NP-complete problems can be transformed into one another in polynomial time.

### Benchmark Experiments

The benchmarking suite evaluates both exact and approximate algorithms on inputs of increasing size.

Key comparisons include:

* Exponential algorithms vs polynomial-time heuristics
* Approximation solution quality vs optimal solutions
* Runtime growth as input size increases

The experiments highlight how exact exponential algorithms quickly become computationally expensive, while heuristics and approximation algorithms provide scalable alternatives.

### Benchmark Outputs

Running the benchmark script produces the following files:

benchmarks/results/runtime_growth.png
benchmarks/results/approximation_quality.png
benchmarks/results/comparison_table.csv

These outputs visualize:

* Runtime growth of exact vs heuristic algorithms
* Approximation ratios for Vertex Cover and TSP
* Tabulated experimental data for further analysis

### Running the Benchmark

From the project root directory:

python -m benchmarks.week8_complexity_benchmark

### Running Tests

To run the full automated test suite:

python -m pytest

All implementations include unit tests verifying correctness and expected algorithm behavior.

### Key Insight

This module demonstrates the practical implications of computational complexity. While many important problems are believed to require exponential time for exact solutions, approximation algorithms and heuristics provide practical methods for obtaining useful solutions within polynomial time.


# GitHub

Full project is hosted here:  
https://github.com/Throwbias/Algorithms_Course.git  

Includes **all source code, tests, benchmarking results, and plots** for verification.

---

## Author

Aaron Tobias  
Master’s Level Algorithms Coursework  
Algorithms and Systems Analysis