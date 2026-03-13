"""
Week 9 - Greedy Facility Location

A practical greedy heuristic:
- Each facility has an opening cost
- Each client has an assignment cost to each facility
- Repeatedly open the facility that gives the best improvement
  in total service cost relative to opening cost
- Assign each client to the cheapest open facility

This is a heuristic implementation for benchmarking and discussion.
"""

import math
from itertools import combinations


def compute_total_cost(open_facilities, opening_costs, assignment_costs):
    """
    Compute total facility location cost.

    Args:
        open_facilities: iterable of facility indices
        opening_costs: list of opening costs
        assignment_costs: matrix assignment_costs[client][facility]

    Returns:
        float total cost
    """
    open_facilities = set(open_facilities)
    if not open_facilities:
        return float("inf")

    open_cost = sum(opening_costs[f] for f in open_facilities)

    assign_cost = 0
    for client_costs in assignment_costs:
        assign_cost += min(client_costs[f] for f in open_facilities)

    return open_cost + assign_cost


def greedy_facility_location(opening_costs, assignment_costs):
    """
    Greedy heuristic for uncapacitated facility location.

    Args:
        opening_costs: list of opening costs per facility
        assignment_costs: matrix [num_clients][num_facilities]

    Returns:
        dict with open_facilities, assignments, total_cost
    """
    num_facilities = len(opening_costs)
    num_clients = len(assignment_costs)

    unopened = set(range(num_facilities))
    open_facilities = set()

    # Start with the single best facility
    best_start = None
    best_cost = float("inf")
    for f in range(num_facilities):
        cost = compute_total_cost({f}, opening_costs, assignment_costs)
        if cost < best_cost:
            best_cost = cost
            best_start = f

    open_facilities.add(best_start)
    unopened.remove(best_start)
    current_cost = best_cost

    improved = True
    while improved and unopened:
        improved = False
        best_candidate = None
        best_candidate_cost = current_cost

        for f in unopened:
            candidate_open = open_facilities | {f}
            cost = compute_total_cost(candidate_open, opening_costs, assignment_costs)
            if cost < best_candidate_cost:
                best_candidate_cost = cost
                best_candidate = f

        if best_candidate is not None:
            open_facilities.add(best_candidate)
            unopened.remove(best_candidate)
            current_cost = best_candidate_cost
            improved = True

    assignments = {}
    for client in range(num_clients):
        best_facility = min(open_facilities, key=lambda f: assignment_costs[client][f])
        assignments[client] = best_facility

    return {
        "open_facilities": sorted(open_facilities),
        "assignments": assignments,
        "total_cost": current_cost
    }


def exact_facility_location(opening_costs, assignment_costs):
    """
    Brute-force exact facility location for small instances.

    Args:
        opening_costs: list of opening costs
        assignment_costs: matrix [client][facility]

    Returns:
        dict with open_facilities, assignments, total_cost
    """
    num_facilities = len(opening_costs)
    best_open = None
    best_cost = float("inf")

    for r in range(1, num_facilities + 1):
        for subset in combinations(range(num_facilities), r):
            cost = compute_total_cost(subset, opening_costs, assignment_costs)
            if cost < best_cost:
                best_cost = cost
                best_open = set(subset)

    assignments = {}
    for client in range(len(assignment_costs)):
        best_facility = min(best_open, key=lambda f: assignment_costs[client][f])
        assignments[client] = best_facility

    return {
        "open_facilities": sorted(best_open),
        "assignments": assignments,
        "total_cost": best_cost
    }