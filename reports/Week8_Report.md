# Week 8 Report — Computational Complexity and Approximation Algorithms

## Executive Summary

Understanding the limits of computation is a fundamental aspect of algorithm design. While many algorithmic problems can be solved efficiently, others appear to require enormous computational resources as input sizes grow. Computational complexity theory provides a framework for classifying these problems and determining which can be solved efficiently and which likely cannot.

This project explored the practical and theoretical aspects of complexity by implementing algorithms from several important categories: exact exponential algorithms, approximation algorithms, and heuristic methods. Specifically, the project included a backtracking solution for the Subset Sum problem, a simple SAT solver for Boolean satisfiability, a 2-approximation algorithm for Vertex Cover, and a nearest-neighbor heuristic for the Traveling Salesman Problem (TSP). In addition, a conceptual reduction from 3-SAT to Vertex Cover was implemented to illustrate how computational problems can be transformed into one another in polynomial time.

Empirical benchmarks compared the runtime growth of exact algorithms against heuristic and approximation approaches. The results demonstrate a clear distinction between exponential-time algorithms and polynomial-time heuristics. Exact methods quickly became computationally expensive as input sizes increased, while approximation algorithms remained efficient and scalable.

These findings illustrate a core insight of computational complexity theory: even when exact optimal solutions are theoretically desirable, practical systems often rely on heuristics and approximation algorithms to produce useful results within reasonable time constraints.

---

## Methodology

The project was implemented in Python within a modular algorithm repository that organizes implementations, benchmarks, and tests into separate directories. The structure allows algorithms to be evaluated systematically and ensures reproducibility through automated tests.

Several categories of algorithms were implemented to illustrate different complexity behaviors.

### Exact Algorithms

Two exact algorithms were implemented to illustrate problems that may require exponential time in the worst case.

**Subset Sum (Backtracking)**
The subset sum problem asks whether a subset of numbers from a given set can sum to a target value. The implemented solution uses recursive backtracking, exploring possible combinations of elements. In the worst case, this approach explores all subsets of the input set, resulting in a time complexity of (O(2^n)). This exponential growth makes the algorithm impractical for large input sizes.

**SAT Solver (Backtracking)**
Boolean satisfiability (SAT) is the problem of determining whether a Boolean formula can be satisfied by some assignment of truth values. A simple backtracking solver was implemented that performs a depth-first search over possible variable assignments. Although the algorithm works for small instances, the number of possible assignments grows exponentially with the number of variables.

### Approximation and Heuristic Algorithms

Because many NP-complete problems are believed to lack efficient exact solutions, approximation algorithms and heuristics are often used in practice.

**Vertex Cover 2-Approximation**
The Vertex Cover problem asks for the smallest set of vertices that covers all edges in a graph. A greedy 2-approximation algorithm was implemented that repeatedly selects an uncovered edge and adds both endpoints to the cover. This guarantees that the solution size will be at most twice the optimal solution, while running in linear time relative to the number of edges.

**Traveling Salesman Nearest Neighbor Heuristic**
The Traveling Salesman Problem seeks the shortest possible route that visits each city exactly once and returns to the origin. The nearest-neighbor heuristic was implemented, which repeatedly travels to the closest unvisited city. While this approach does not guarantee optimality, it runs efficiently with time complexity (O(n^2)).

### Polynomial-Time Reduction

To illustrate the concept of NP-completeness, a conceptual reduction from **3-SAT to Vertex Cover** was implemented. Reductions are transformations that convert instances of one problem into instances of another in polynomial time. If such a transformation exists, solving the second problem efficiently would imply an efficient solution for the first.

The reduction demonstrates how variables and clauses from a SAT instance can be represented using graph structures, highlighting how seemingly different problems can encode equivalent computational difficulty.

### Benchmarking Approach

Benchmarks were conducted using randomly generated inputs of increasing size. The benchmarking script measured runtime and solution quality for each algorithm.

Three primary outputs were produced:

* `runtime_growth.png` — showing algorithm runtime as input size increases
* `approximation_quality.png` — illustrating approximation ratios relative to optimal solutions
* `comparison_table.csv` — containing detailed runtime and solution data

These experiments allowed empirical comparisons between exact and approximate algorithms.

---

## Results

The experimental results demonstrate clear differences in scalability between algorithm classes.

### Runtime Growth

The runtime comparison plot shows that the backtracking subset sum algorithm experiences rapid growth as input size increases. This behavior reflects the exponential number of subsets that must be explored. Even moderate increases in input size result in substantial increases in runtime.

In contrast, heuristic and approximation algorithms maintained stable performance across larger input sizes. The greedy subset sum heuristic and nearest-neighbor TSP algorithm completed almost instantly even as input sizes increased.

These results illustrate the practical consequences of exponential complexity. While exact algorithms may work for small inputs, their runtime quickly becomes prohibitive.

### Approximation Quality

The approximation quality plot compares heuristic solutions against optimal results for smaller problem instances.

For the Vertex Cover problem, the approximation algorithm consistently produced solutions within the expected theoretical bound of twice the optimal size. In most cases, the approximation ratio was significantly better than the worst-case guarantee.

The TSP nearest-neighbor heuristic also produced reasonably good routes, although the quality varied depending on the spatial arrangement of cities. This variability is expected for heuristic algorithms that rely on local decisions.

### Comparison Table

The benchmark results were also exported to a CSV file containing runtime measurements, input sizes, and approximation ratios. This structured data provides a clear record of algorithm performance and enables further analysis.

Overall, the experiments demonstrate that while exact algorithms guarantee optimal solutions, approximation algorithms provide a practical balance between runtime and solution quality.

---

## Discussion

One of the central questions in computer science is the relationship between the complexity classes **P** and **NP**. Problems in class P can be solved in polynomial time, meaning their runtime grows relatively slowly as input size increases. In contrast, NP problems are those whose solutions can be verified efficiently but may not be solvable efficiently.

NP-complete problems represent the hardest problems in NP. If any NP-complete problem were solved in polynomial time, every problem in NP would also become efficiently solvable. Despite decades of research, no polynomial-time solution has been found for any NP-complete problem.

The reduction from 3-SAT to Vertex Cover illustrates how NP-complete problems are connected. Through polynomial-time reductions, researchers have shown that many seemingly unrelated problems share the same fundamental computational difficulty.

Because exact solutions may be impractical for large instances, approximation algorithms and heuristics play a crucial role in real-world systems. For example, logistics companies often rely on heuristic solutions to routing problems rather than attempting to compute exact optimal routes.

The experiments conducted in this project reinforce this idea. Exact algorithms quickly became impractical as input sizes increased, while approximation algorithms remained efficient and produced useful solutions.

This trade-off between optimality and efficiency is a key consideration in algorithm design. In many applications, obtaining a near-optimal solution quickly is far more valuable than computing an exact solution that requires excessive computational resources.

---

## Conclusion

This project explored both the theoretical and practical aspects of computational complexity. By implementing exact algorithms, approximation algorithms, and reductions between problems, the project demonstrates how algorithm designers approach computationally difficult problems.

The empirical benchmarks clearly illustrate the dramatic difference between exponential and polynomial runtime growth. Exact algorithms, while theoretically correct, become impractical as problem sizes increase. Approximation algorithms and heuristics, on the other hand, provide scalable alternatives that deliver useful solutions efficiently.

The reduction example highlights another important insight: many difficult problems are deeply interconnected through polynomial-time transformations. Understanding these relationships helps researchers classify problems and identify which techniques may be applicable.

Ultimately, computational complexity theory does not simply describe the limits of computation; it guides practical algorithm design. By recognizing when exact solutions are infeasible, algorithm designers can develop heuristics and approximations that enable real-world systems to function effectively.

Through this combination of theory, implementation, and experimentation, this project provides a comprehensive exploration of the limits and possibilities of algorithmic problem solving.
