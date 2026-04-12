## String Search Project
## Week 13 – Advanced Data Structures

This week focused on implementing advanced data structures and cache-oblivious algorithms with practical applications and benchmarking.

### Implemented Components

#### Tree-Based Range Query Structures
- **Segment Tree**
  - Range sum queries
  - Point updates
  - Lazy propagation for efficient range updates
- **Fenwick Tree (Binary Indexed Tree)**
  - Prefix sums
  - Range sums via prefix differences
  - Point updates
- **Persistent Segment Tree**
  - Versioned updates through path copying
  - Historical queries across previous versions

#### Succinct and Compressed Structures
- **Bit Vector**
  - Access
  - `rank1`, `rank0`
  - `select1`, `select0`
- **Rank/Select Wrapper**
  - Clean interface over bit-vector operations
- **Wavelet Tree**
  - Frequency queries
  - Rank queries
  - Quantile queries
  - DNA-oriented symbolic indexing support

#### Cache-Oblivious Algorithms
- **Matrix Operations**
  - Naive transpose
  - Cache-oblivious transpose
  - Naive matrix multiplication
  - Recursive cache-oblivious multiplication
- **Layouts**
  - Balanced BST construction
  - Level-order layout
  - Recursive cache-friendly layout
  - Locality comparison utilities

#### Applications
- **Range Query Engine**
  - Unified interface over Segment Tree, Fenwick Tree, and Persistent Tree
- **DNA Index**
  - Range counting
  - k-th smallest nucleotide queries
  - Pattern frequency queries
- **Version Control Prototype**
  - Versioned file states
  - Commit history
  - Diff support across versions

#### Benchmarking
Benchmark suite added for:
- Segment Tree vs Fenwick Tree
- Persistent tree overhead
- Bit-vector rank/select performance
- Wavelet tree performance and compression proxy
- Cache-oblivious vs naive matrix operations

Benchmark outputs are written to:

```text
results/week13/

# GitHub

Full project is hosted here:  
https://github.com/Throwbias/Algorithms_Course.git  

Includes **all source code, tests, benchmarking results, and plots** for verification.

---

## Author

Aaron Tobias  
Master’s Level Algorithms Coursework  
Algorithms and Systems Analysis