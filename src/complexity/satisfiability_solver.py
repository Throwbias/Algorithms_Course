"""
Simple SAT solver using DFS/backtracking for small CNF formulas.
Literals are represented as integers:
  1  -> x1
 -1  -> not x1
  2  -> x2
 etc.
"""

import random


def evaluate_literal(literal, assignment):
    var = abs(literal)
    if var not in assignment:
        return None
    value = assignment[var]
    return value if literal > 0 else not value


def evaluate_clause(clause, assignment):
    undecided = False
    for literal in clause:
        result = evaluate_literal(literal, assignment)
        if result is True:
            return True
        if result is None:
            undecided = True
    if undecided:
        return None
    return False


def evaluate_cnf(cnf, assignment):
    all_true = True
    for clause in cnf:
        result = evaluate_clause(clause, assignment)
        if result is False:
            return False
        if result is None:
            all_true = False
    return True if all_true else None


def solve_sat_backtracking(cnf, num_vars, assignment=None, var=1):
    if assignment is None:
        assignment = {}

    status = evaluate_cnf(cnf, assignment)
    if status is True:
        return assignment.copy()
    if status is False:
        return None

    if var > num_vars:
        return None

    assignment[var] = True
    result = solve_sat_backtracking(cnf, num_vars, assignment, var + 1)
    if result is not None:
        return result

    assignment[var] = False
    result = solve_sat_backtracking(cnf, num_vars, assignment, var + 1)
    if result is not None:
        return result

    del assignment[var]
    return None


def random_sat_heuristic(cnf, num_vars, trials=500):
    for _ in range(trials):
        assignment = {var: random.choice([True, False]) for var in range(1, num_vars + 1)}
        if evaluate_cnf(cnf, assignment) is True:
            return assignment
    return None