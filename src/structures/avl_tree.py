from __future__ import annotations
from typing import Optional, List

class AVLNode:
    """Node for AVL Tree."""
    def __init__(self, key: int):
        self.key: int = key
        self.left: Optional[AVLNode] = None
        self.right: Optional[AVLNode] = None
        self.height: int = 1  # Height of node


class AVLTree:
    """Balanced Binary Search Tree (AVL) with rotations."""

    def __init__(self):
        self.root: Optional[AVLNode] = None

    # -------------------- HELPER METHODS --------------------
    def _get_height(self, node: Optional[AVLNode]) -> int:
        if not node:
            return 0
        return node.height

    def _get_balance(self, node: Optional[AVLNode]) -> int:
        """Balance factor = height(left) - height(right)."""
        if not node:
            return 0
        return self._get_height(node.left) - self._get_height(node.right)

    def _right_rotate(self, y: AVLNode) -> AVLNode:
        """Right rotation."""
        x = y.left
        T2 = x.right

        # Perform rotation
        x.right = y
        y.left = T2

        # Update heights
        y.height = max(self._get_height(y.left), self._get_height(y.right)) + 1
        x.height = max(self._get_height(x.left), self._get_height(x.right)) + 1

        return x

    def _left_rotate(self, x: AVLNode) -> AVLNode:
        """Left rotation."""
        y = x.right
        T2 = y.left

        # Perform rotation
        y.left = x
        x.right = T2

        # Update heights
        x.height = max(self._get_height(x.left), self._get_height(x.right)) + 1
        y.height = max(self._get_height(y.left), self._get_height(y.right)) + 1

        return y

    # -------------------- INSERTION --------------------
    def insert(self, key: int):
        """Public insert method."""
        self.root = self._insert(self.root, key)

    def _insert(self, node: Optional[AVLNode], key: int) -> AVLNode:
        if not node:
            return AVLNode(key)

        # Normal BST insertion
        if key < node.key:
            node.left = self._insert(node.left, key)
        elif key > node.key:
            node.right = self._insert(node.right, key)
        else:
            # Duplicate keys not allowed
            return node

        # Update height
        node.height = 1 + max(self._get_height(node.left), self._get_height(node.right))

        # Check balance
        balance = self._get_balance(node)

        # Rebalance if needed
        # Left Left
        if balance > 1 and key < node.left.key:
            return self._right_rotate(node)
        # Right Right
        if balance < -1 and key > node.right.key:
            return self._left_rotate(node)
        # Left Right
        if balance > 1 and key > node.left.key:
            node.left = self._left_rotate(node.left)
            return self._right_rotate(node)
        # Right Left
        if balance < -1 and key < node.right.key:
            node.right = self._right_rotate(node.right)
            return self._left_rotate(node)

        return node

    # -------------------- DELETION --------------------
    def delete(self, key: int):
        """Public delete method."""
        self.root = self._delete(self.root, key)

    def _delete(self, node: Optional[AVLNode], key: int) -> Optional[AVLNode]:
        if not node:
            return node

        # Standard BST deletion
        if key < node.key:
            node.left = self._delete(node.left, key)
        elif key > node.key:
            node.right = self._delete(node.right, key)
        else:
            # Node with only one child or no child
            if not node.left:
                return node.right
            elif not node.right:
                return node.left

            # Node with two children: get inorder successor
            temp = self._get_min_value_node(node.right)
            node.key = temp.key
            node.right = self._delete(node.right, temp.key)

        # Update height
        node.height = 1 + max(self._get_height(node.left), self._get_height(node.right))

        # Rebalance
        balance = self._get_balance(node)

        # Left Left
        if balance > 1 and self._get_balance(node.left) >= 0:
            return self._right_rotate(node)
        # Left Right
        if balance > 1 and self._get_balance(node.left) < 0:
            node.left = self._left_rotate(node.left)
            return self._right_rotate(node)
        # Right Right
        if balance < -1 and self._get_balance(node.right) <= 0:
            return self._left_rotate(node)
        # Right Left
        if balance < -1 and self._get_balance(node.right) > 0:
            node.right = self._right_rotate(node.right)
            return self._left_rotate(node)

        return node

    def _get_min_value_node(self, node: AVLNode) -> AVLNode:
        current = node
        while current.left:
            current = current.left
        return current

    # -------------------- SEARCH --------------------
    def search(self, key: int) -> bool:
        """Search for key in AVL Tree."""
        node = self.root
        while node:
            if key == node.key:
                return True
            elif key < node.key:
                node = node.left
            else:
                node = node.right
        return False

    # -------------------- TRAVERSAL --------------------
    def in_order_traversal(self) -> List[int]:
        """Return keys in sorted order."""
        result: List[int] = []

        def _in_order(node: Optional[AVLNode]):
            if not node:
                return
            _in_order(node.left)
            result.append(node.key)
            _in_order(node.right)

        _in_order(self.root)
        return result

    # -------------------- HEIGHT --------------------
    def height(self) -> int:
        """Return height of the tree."""
        return self._get_height(self.root)
