from typing import Any, Optional, List, Tuple

class HashTable:
    """
    Hash Table supporting:
    - Separate chaining (linked lists)
    - Open addressing (linear probing)

    Operations:
    - insert(key, value)
    - get(key)
    - delete(key)

    Automatic resizing based on load factor.
    """

    def __init__(self, capacity: int = 16, method: str = "chaining"):
        self.capacity = capacity
        self.size = 0
        self.method = method.lower()
        self.load_factor_threshold = 0.7

        if self.method == "chaining":
            self.table: List[List[Tuple[Any, Any]]] = [[] for _ in range(capacity)]
        elif self.method == "linear":
            self.table: List[Optional[Tuple[Any, Any]]] = [None] * capacity
        else:
            raise ValueError("method must be 'chaining' or 'linear'")

    # -------------------- HASH FUNCTION --------------------
    def _hash(self, key: Any) -> int:
        return hash(key) % self.capacity

    # -------------------- RESIZE --------------------
    def _resize(self):
        old_capacity = self.capacity
        old_table = self.table
        self.capacity *= 2
        self.size = 0

        if self.method == "chaining":
            self.table = [[] for _ in range(self.capacity)]
            for bucket in old_table:
                for key, value in bucket:
                    self.insert(key, value)
        else:  # linear probing
            self.table = [None] * self.capacity
            for item in old_table:
                if item is not None:
                    self.insert(item[0], item[1])

    # -------------------- INSERT --------------------
    def insert(self, key: Any, value: Any):
        if self.size / self.capacity >= self.load_factor_threshold:
            self._resize()

        idx = self._hash(key)

        if self.method == "chaining":
            # Replace if key exists
            for i, (k, _) in enumerate(self.table[idx]):
                if k == key:
                    self.table[idx][i] = (key, value)
                    return
            self.table[idx].append((key, value))
            self.size += 1
        else:  # linear probing
            start_idx = idx
            while self.table[idx] is not None:
                if self.table[idx][0] == key:
                    self.table[idx] = (key, value)
                    return
                idx = (idx + 1) % self.capacity
                if idx == start_idx:
                    raise RuntimeError("Hashtable full, even after resize")
            self.table[idx] = (key, value)
            self.size += 1

    # -------------------- GET --------------------
    def get(self, key: Any) -> Optional[Any]:
        idx = self._hash(key)
        if self.method == "chaining":
            for k, v in self.table[idx]:
                if k == key:
                    return v
            return None
        else:  # linear probing
            start_idx = idx
            while self.table[idx] is not None:
                if self.table[idx][0] == key:
                    return self.table[idx][1]
                idx = (idx + 1) % self.capacity
                if idx == start_idx:
                    break
            return None

    # -------------------- DELETE --------------------
    def delete(self, key: Any):
        idx = self._hash(key)
        if self.method == "chaining":
            for i, (k, _) in enumerate(self.table[idx]):
                if k == key:
                    del self.table[idx][i]
                    self.size -= 1
                    return
        else:  # linear probing
            start_idx = idx
            while self.table[idx] is not None:
                if self.table[idx][0] == key:
                    self.table[idx] = None
                    self.size -= 1
                    # rehash cluster after deletion
                    next_idx = (idx + 1) % self.capacity
                    while self.table[next_idx] is not None:
                        k, v = self.table[next_idx]
                        self.table[next_idx] = None
                        self.size -= 1
                        self.insert(k, v)
                        next_idx = (next_idx + 1) % self.capacity
                    return
                idx = (idx + 1) % self.capacity
                if idx == start_idx:
                    break

    # -------------------- UTILITY --------------------
    def __len__(self):
        return self.size

    def __str__(self):
        return str(self.table)
