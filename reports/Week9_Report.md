# Week 9 Report: Approximation Algorithms

## Introduction

Many important optimization problems are NP-hard, meaning that no known polynomial-time algorithm can guarantee an exact optimal solution for every instance. Approximation algorithms address this challenge by producing solutions efficiently while providing guarantees about how close those solutions are to optimal. In this project, approximation strategies were implemented for several classical optimization problems, including Vertex Cover, Set Cover, Facility Location, Metric Traveling Salesman Problem (TSP), and Max-Cut.

## Algorithms Implemented

### Vertex Cover 2-Approximation
The vertex cover algorithm repeatedly selects an uncovered edge and adds both endpoints to the cover. This produces a valid cover whose size is at most twice the size of the optimal solution.

### Set Cover via LP Relaxation and Rounding
Set Cover was implemented using linear programming relaxation with threshold rounding. When an LP solver was unavailable, a greedy fallback method was used. This approach demonstrates how relaxed continuous solutions can guide discrete approximations.

### Greedy Facility Location
A greedy heuristic was used for facility location. Facilities were opened only when they reduced the total combined opening and assignment cost. Although this implementation is heuristic-based, it performs well on small benchmark instances.

### Metric TSP 2-Approximation
For metric TSP, a minimum spanning tree (MST) was computed and traversed in preorder. Because the distance function satisfies the triangle inequality, the resulting tour has cost at most twice the optimal tour.

### Randomized Max-Cut
The Max-Cut algorithm used repeated randomized bipartitions of the graph and selected the best cut found. The expected cut value for a single random partition is at least half of optimal, and repeated trials improve empirical performance.

## Experimental Setup

All algorithms were implemented in Python. Small benchmark instances were generated synthetically so that exact optimal solutions could also be computed by brute force. This allowed direct comparison between approximate and optimal values. Runtime, solution quality, and approximation ratio were recorded in a CSV file, and plots were produced to visualize performance.

## Results

The benchmark results showed that all approximation algorithms ran quickly on the tested inputs. In most cases, the empirical solution quality was better than the worst-case approximation bound. The Vertex Cover and Metric TSP implementations behaved consistently with their theoretical guarantees. The randomized Max-Cut implementation often produced cuts close to optimal after multiple trials. Set Cover and Facility Location also performed competitively on the generated instances.

## Discussion

This project demonstrated the practical value of approximation algorithms when exact optimization is computationally expensive. Theoretical approximation bounds provide a worst-case guarantee, while empirical benchmarking shows that real performance is often stronger. The combination of provable analysis and experimental evidence makes approximation methods especially useful in applied algorithm design.

## Conclusion

Approximation algorithms offer a practical response to NP-hard optimization problems. Rather than treating intractability as a dead end, they provide efficient methods for producing solutions that are close to optimal. This project illustrated how greedy design, LP relaxation, and randomization can all be used to solve difficult optimization problems effectively in practice.