# Week 3 – Data Structure Benchmarking

This project benchmarks multiple core data structures to compare their **insert**, **search**, and **delete** performance across increasing input sizes. The goal is to move beyond theoretical Big-O and see how these structures behave in practice.

All benchmarks were run locally using Python and timed with `time.perf_counter()`.

https://github.com/Throwbias/Algorithms_Course
---

## Data Structures Implemented

The following structures were implemented from scratch (no built-ins):

- **Binary Heap**
  - Min Heap
  - Max Heap
- **AVL Tree**
- **Hash Table**
  - Separate Chaining
  - Linear Probing

Each structure supports insert, search, and delete operations where applicable.

---

## Benchmark Methodology

For each input size, the following steps were performed:

1. Generate random integer data
2. Insert all values into the structure
3. Search for a subset of values
4. Delete all values

Input sizes tested:
- `1,000`
- `10,000`
- `100,000`

Timing results are recorded in seconds and averaged per operation type.

---

## Benchmark Results

Raw benchmark output (CSV format):

size,insert_minheap,insert_maxheap,search_minheap,search_maxheap,delete_minheap,delete_maxheap,insert_avl,search_avl,delete_avl,insert_ht_chain,search_ht_chain,delete_ht_chain,insert_ht_linear,search_ht_linear,delete_ht_linear
1000,0.000594,0.000587,0.000457,0.000399,0.003490,0.003514,0.004262,0.000937,0.004972,0.002119,0.000406,0.000494,0.001166,0.000352,0.000829
10000,0.006420,0.006133,0.004987,0.004051,0.054002,0.055831,0.057780,0.007495,0.060079,0.023086,0.004099,0.005936,0.011642,0.007314,0.029907
100000,0.066621,0.060735,0.048596,0.070195,0.780969,0.788908,0.788842,0.101426,0.737122,0.269620,0.061431,0.076987,0.163288,0.050961,0.082193


---

## Observations

- **Heaps**
  - Insert and search scale well
  - Delete becomes expensive at larger sizes due to repeated reheapification

- **AVL Tree**
  - Consistent performance across all operations
  - Higher insert/delete cost due to rebalancing, but predictable scaling

- **Hash Table (Chaining)**
  - Strong overall performance
  - Search remains fast even at higher sizes

- **Hash Table (Linear Probing)**
  - Fast inserts and searches at small sizes
  - Performance degrades as collisions increase

These results align closely with theoretical expectations while highlighting real-world tradeoffs.

---

## Running the Benchmarks

From the project root:

```bash
python -m benchmarks.week3_structures_benchmark
Plots are generated automatically and saved to the output directory.

Project Structure
.
├── structures/
│   ├── binary_heap.py
│   ├── avl_tree.py
│   ├── hash_table.py
│
├── benchmarks/
│   └── week3_structures_benchmark.py
│
├── plots/
│   └── *.png
│
└── README.md
Notes
All implementations are educational and written for clarity

No Python built-in data structures were used for core logic

Benchmarks were run on a local machine; absolute timings may vary, trends should not