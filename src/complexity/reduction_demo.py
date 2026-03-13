"""
Educational demonstration of a polynomial-time reduction
from 3-SAT to Vertex Cover.

This module does not attempt to solve large instances.
It illustrates the mapping structure used in the classic reduction.
"""


class ThreeSATInstance:
    def __init__(self, num_vars, clauses):
        self.num_vars = num_vars
        self.clauses = clauses


class VertexCoverInstance:
    def __init__(self, vertices, edges, k):
        self.vertices = vertices
        self.edges = edges
        self.k = k


def literal_name(literal):
    return f"x{literal}" if literal > 0 else f"~x{abs(literal)}"


def reduce_3sat_to_vertex_cover(instance):
    vertices = set()
    edges = set()
    steps = []

    steps.append("Step 1: Create a pair of variable vertices for each Boolean variable.")

    for i in range(1, instance.num_vars + 1):
        pos = f"x{i}"
        neg = f"~x{i}"
        vertices.add(pos)
        vertices.add(neg)
        edges.add(tuple(sorted((pos, neg))))
        steps.append(f"Variable x{i}: created vertices {pos} and {neg}, with an edge between them.")

    steps.append("Step 2: Create a 3-node clause gadget (triangle) for each clause.")

    for clause_index, clause in enumerate(instance.clauses, start=1):
        clause_nodes = []
        for lit_index, literal in enumerate(clause, start=1):
            node = f"C{clause_index}_{lit_index}:{literal_name(literal)}"
            clause_nodes.append(node)
            vertices.add(node)

        a, b, c = clause_nodes
        edges.add(tuple(sorted((a, b))))
        edges.add(tuple(sorted((b, c))))
        edges.add(tuple(sorted((a, c))))

        steps.append(
            f"Clause {clause_index}: created triangle gadget with nodes "
            f"{clause_nodes[0]}, {clause_nodes[1]}, {clause_nodes[2]}."
        )

        for node, literal in zip(clause_nodes, clause):
            target = literal_name(literal)
            edges.add(tuple(sorted((node, target))))
            steps.append(f"Connected {node} to variable-literal node {target}.")

    k = instance.num_vars + 2 * len(instance.clauses)
    steps.append(
        f"Step 3: Set target cover size k = n + 2m = {instance.num_vars} + 2({len(instance.clauses)}) = {k}."
    )

    vc_instance = VertexCoverInstance(vertices=sorted(vertices), edges=sorted(edges), k=k)
    return vc_instance, steps


def explain_reduction(instance):
    vc_instance, steps = reduce_3sat_to_vertex_cover(instance)
    explanation = "\n".join(steps)
    return vc_instance, explanation