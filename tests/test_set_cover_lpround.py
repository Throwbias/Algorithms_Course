from src.approximation.set_cover_lpround import (
    set_cover_lp_relaxation_rounding,
    exact_set_cover,
)


def test_set_cover_valid_solution():
    universe = {1, 2, 3, 4}
    sets = [{1, 2}, {2, 3}, {3, 4}, {1, 4}]
    costs = [1, 1, 1, 1]

    result = set_cover_lp_relaxation_rounding(universe, sets, costs)

    covered = set()
    for s in result["selected_sets"]:
        covered |= s

    assert covered == universe


def test_set_cover_cost_at_least_optimal():
    universe = {1, 2, 3}
    sets = [{1, 2}, {2, 3}, {1, 3}]
    costs = [1, 1, 1]

    approx_result = set_cover_lp_relaxation_rounding(universe, sets, costs)
    optimal_result = exact_set_cover(universe, sets, costs)

    assert approx_result["total_cost"] >= optimal_result["total_cost"]