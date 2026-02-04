# src/graphs/graph.py

class Graph:
    def __init__(self, directed=False, weighted=False, representation="list"):
        self.directed = directed
        self.weighted = weighted
        self.representation = representation  # "list" or "matrix"
        self.nodes = []
        self.adj_list = {} if representation == "list" else None
        self.adj_matrix = [] if representation == "matrix" else None

    def add_node(self, node):
        if node not in self.nodes:
            self.nodes.append(node)
            if self.representation == "list":
                self.adj_list[node] = []
            elif self.representation == "matrix":
                n = len(self.nodes)
                # Expand existing rows
                for row in self.adj_matrix:
                    row.append(0)
                # Add new row
                self.adj_matrix.append([0] * n)

    def add_edge(self, u, v, weight=1):
        self.add_node(u)
        self.add_node(v)
        w = weight if self.weighted else 1

        if self.representation == "list":
            if self.weighted:
                self.adj_list[u].append((v, w))
            else:
                self.adj_list[u].append(v)
            if not self.directed:
                if self.weighted:
                    self.adj_list[v].append((u, w))
                else:
                    self.adj_list[v].append(u)
        else:  # matrix
            i, j = self.nodes.index(u), self.nodes.index(v)
            self.adj_matrix[i][j] = w
            if not self.directed:
                self.adj_matrix[j][i] = w

    def get_neighbors(self, node):
        if self.representation == "list":
            if self.weighted:
                return self.adj_list.get(node, [])
            else:
                #Convert unweighted neighbors to (neighbor, 1) format
                return [(v, 1) for v in self.adj_list.get(node, [])]
        else: # matrix
            i = self.nodes.index(node)
            neighbors = []
            for j, val in enumerate(self.adj_matrix[i]):
                if val != 0:
                    neighbors.append((self.nodes[j], val))
            return neighbors

    def has_edge(self, u, v):
        return v in [n if not self.weighted else n for n, *_ in self.get_neighbors(u)] if self.representation == "list" else any(
            self.nodes[j] == v and self.adj_matrix[self.nodes.index(u)][j] != 0 for j in range(len(self.nodes))
        )

    def __str__(self):
        if self.representation == "list":
            return "\n".join(f"{u}: {self.adj_list[u]}" for u in self.nodes)
        else:
            return "\n".join("\t".join(map(str, row)) for row in self.adj_matrix)