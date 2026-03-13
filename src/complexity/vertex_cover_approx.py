"""
2-Approximation Algorithm for Vertex Cover
"""

def vertex_cover_approx(edges):
    cover = set()
    edges = edges.copy()

    while edges:
        u, v = edges.pop()

        cover.add(u)
        cover.add(v)

        edges = {
            (a, b)
            for (a, b) in edges
            if a not in (u, v) and b not in (u, v)
        }

    return cover


def is_vertex_cover(edges, cover):
    for u, v in edges:
        if u not in cover and v not in cover:
            return False
    return True