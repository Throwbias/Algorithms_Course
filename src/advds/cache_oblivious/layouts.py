from collections import deque


class BinaryTreeNode:
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right


def build_balanced_bst(sorted_values):
    """
    Build a balanced binary tree from sorted values.
    """
    if not sorted_values:
        return None

    mid = len(sorted_values) // 2
    return BinaryTreeNode(
        sorted_values[mid],
        build_balanced_bst(sorted_values[:mid]),
        build_balanced_bst(sorted_values[mid + 1:]),
    )


def inorder_values(root):
    if root is None:
        return []
    return inorder_values(root.left) + [root.value] + inorder_values(root.right)


def level_order_layout(root):
    """
    Standard breadth-first / heap-like layout.
    """
    if root is None:
        return []

    layout = []
    queue = deque([root])

    while queue:
        node = queue.popleft()
        layout.append(node.value)

        if node.left is not None:
            queue.append(node.left)
        if node.right is not None:
            queue.append(node.right)

    return layout


def veb_layout(root):
    """
    Practical recursive cache-friendly layout.
    This is not a full formal vEB decomposition by height,
    but it captures the same idea: recursively place root,
    then recursively place subtrees in contiguous memory.
    """
    layout = []

    def recurse(node):
        if node is None:
            return
        layout.append(node.value)
        recurse(node.left)
        recurse(node.right)

    recurse(root)
    return layout


def index_map(layout):
    return {value: i for i, value in enumerate(layout)}


def path_to_value(root, target):
    """
    Return root-to-target path as a list of node values.
    Assumes BST ordering.
    """
    path = []
    node = root

    while node is not None:
        path.append(node.value)
        if target == node.value:
            return path
        elif target < node.value:
            node = node.left
        else:
            node = node.right

    return []


def path_memory_cost(layout, path):
    """
    Simple locality proxy:
    sum of absolute jumps between consecutive node indices in memory layout.
    Smaller is better.
    """
    if len(path) <= 1:
        return 0

    pos = index_map(layout)
    cost = 0
    for i in range(1, len(path)):
        cost += abs(pos[path[i]] - pos[path[i - 1]])
    return cost


def compare_locality(root, targets):
    """
    Compare average path memory cost for level-order vs vEB-style layout.
    """
    level_layout = level_order_layout(root)
    veb = veb_layout(root)

    level_costs = []
    veb_costs = []

    for target in targets:
        path = path_to_value(root, target)
        if not path:
            continue
        level_costs.append(path_memory_cost(level_layout, path))
        veb_costs.append(path_memory_cost(veb, path))

    avg_level = sum(level_costs) / len(level_costs) if level_costs else 0
    avg_veb = sum(veb_costs) / len(veb_costs) if veb_costs else 0

    return {
        "level_order_layout": level_layout,
        "veb_layout": veb,
        "average_level_order_cost": avg_level,
        "average_veb_cost": avg_veb,
    }