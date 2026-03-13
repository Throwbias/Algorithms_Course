"""
Week 9 - Set Cover Approximation

Includes:
1. LP relaxation + simple threshold rounding
2. Greedy set cover fallback/baseline

For the LP-based version:
- Minimize sum(x_i)
- Subject to each element being covered:
    sum(x_i for sets containing element) >= 1
- 0 <= x_i <= 1

Then round using threshold 1 / f,
where f is the maximum number of sets containing any single element.
"""

from itertools import combinations

try:
    import pulp
except ImportError:
    pulp = None


def greedy_set_cover(universe, sets, costs=None):
    """
    Greedy approximation for set cover.

    Args:
        universe: set of elements to cover
        sets: list of sets
        costs: optional list of costs; defaults to all 1

    Returns:
        dict with selected_indices, selected_sets, total_cost
    """
    universe = set(universe)
    sets = [set(s) for s in sets]
    if costs is None:
        costs = [1] * len(sets)

    uncovered = set(universe)
    selected = []

    while uncovered:
        best_idx = None
        best_score = -1

        for i, s in enumerate(sets):
            newly_covered = len(uncovered & s)
            if newly_covered == 0:
                continue
            score = newly_covered / costs[i]
            if score > best_score:
                best_score = score
                best_idx = i

        if best_idx is None:
            raise ValueError("Universe cannot be fully covered by provided sets.")

        selected.append(best_idx)
        uncovered -= sets[best_idx]

    total_cost = sum(costs[i] for i in selected)
    return {
        "selected_indices": selected,
        "selected_sets": [sets[i] for i in selected],
        "total_cost": total_cost
    }


def set_cover_lp_relaxation_rounding(universe, sets, costs=None):
    """
    LP relaxation + threshold rounding for set cover.

    If PuLP is unavailable, falls back to greedy set cover.

    Args:
        universe: set of elements
        sets: list of sets
        costs: optional list of costs

    Returns:
        dict with selected_indices, selected_sets, total_cost, method
    """
    universe = set(universe)
    sets = [set(s) for s in sets]

    if costs is None:
        costs = [1] * len(sets)

    if pulp is None:
        result = greedy_set_cover(universe, sets, costs)
        result["method"] = "greedy_fallback"
        return result

    # Frequency f = max number of sets containing any element
    element_frequencies = {}
    for e in universe:
        freq = sum(1 for s in sets if e in s)
        if freq == 0:
            raise ValueError(f"Element {e} is not covered by any set.")
        element_frequencies[e] = freq

    f = max(element_frequencies.values())
    threshold = 1 / f

    problem = pulp.LpProblem("SetCoverLP", pulp.LpMinimize)
    x = [pulp.LpVariable(f"x_{i}", lowBound=0, upBound=1) for i in range(len(sets))]

    # Objective
    problem += pulp.lpSum(costs[i] * x[i] for i in range(len(sets)))

    # Coverage constraints
    for e in universe:
        problem += pulp.lpSum(x[i] for i, s in enumerate(sets) if e in s) >= 1

    problem.solve(pulp.PULP_CBC_CMD(msg=False))

    selected = [i for i in range(len(sets)) if x[i].value() is not None and x[i].value() >= threshold]

    covered = set()
    for i in selected:
        covered |= sets[i]

    # If rounding misses something, complete with greedy
    if covered != universe:
        uncovered = universe - covered
        remaining_indices = [i for i in range(len(sets)) if i not in selected]

        while uncovered:
            best_idx = None
            best_score = -1
            for i in remaining_indices:
                newly_covered = len(uncovered & sets[i])
                if newly_covered == 0:
                    continue
                score = newly_covered / costs[i]
                if score > best_score:
                    best_score = score
                    best_idx = i

            if best_idx is None:
                raise ValueError("Universe cannot be fully covered after rounding.")

            selected.append(best_idx)
            uncovered -= sets[best_idx]
            remaining_indices.remove(best_idx)

    total_cost = sum(costs[i] for i in selected)
    return {
        "selected_indices": selected,
        "selected_sets": [sets[i] for i in selected],
        "total_cost": total_cost,
        "method": "lp_rounding",
        "threshold": threshold
    }


def exact_set_cover(universe, sets, costs=None):
    """
    Brute-force exact minimum set cover for small inputs.

    Args:
        universe: set of elements
        sets: list of sets
        costs: optional list of costs

    Returns:
        dict with selected_indices, total_cost
    """
    universe = set(universe)
    sets = [set(s) for s in sets]

    if costs is None:
        costs = [1] * len(sets)

    n = len(sets)
    best_subset = None
    best_cost = float("inf")

    for r in range(1, n + 1):
        for subset in combinations(range(n), r):
            covered = set()
            cost = 0
            for i in subset:
                covered |= sets[i]
                cost += costs[i]

            if covered == universe and cost < best_cost:
                best_subset = list(subset)
                best_cost = cost

    if best_subset is None:
        raise ValueError("Universe cannot be fully covered.")

    return {
        "selected_indices": best_subset,
        "selected_sets": [sets[i] for i in best_subset],
        "total_cost": best_cost
    }