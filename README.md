# Algorithms Course — Week 5: Dynamic Programming

## Overview
This week focuses on **Dynamic Programming (DP)**, demonstrating how recursion can be optimized with memoization and tabulation for problems with overlapping subproblems.

Implemented DP problems:
- Fibonacci Sequence
- 0/1 Knapsack Problem
- Longest Common Subsequence (LCS)

Benchmarks compare **naive recursion** vs **top-down memoization** vs **bottom-up tabulation**.

## Project Structure
week5_project/
├── README.md
├── src/
│ ├── dp/
│ │ ├── fibonacci.py
│ │ ├── knapsack.py
│ │ └── lcs.py
│ └── utils/
│ └── visualization.py
├── benchmarks/
│ ├── week5_dp_benchmark.py
│ └── results/
├── tests/
├── analysis/
└── examples/

## Running Benchmarks

```bash
# Activate virtual environment
source venv/Scripts/activate  # Windows: venv\Scripts\activate

# Run the Week 5 benchmark
python -m benchmarks.week5_dp_benchmark

All benchmark CSVs and performance PNGs are saved to benchmarks/results/.

## Tests

Run all tests for Week 5:
pytest tests/test_fibonacci.py -v
pytest tests/test_knapsack.py -v
pytest tests/test_lcs.py -v

Check out the full project here:
https://github.com/AaronTobias/Algorithms_Course