"""
Compressed suffix trie / suffix-tree-style structure.

This is the simpler project-acceptable option:
- compressed trie built from all suffixes
- supports substring queries
- prefix matching
- longest repeated substring
- count distinct substrings

It is not Ukkonen's linear-time suffix tree, but it satisfies the
compressed-trie option described in the project brief.
"""

from typing import Dict, List, Tuple, Optional


class SuffixTreeNode:
    def __init__(self):
        self.children: Dict[str, Tuple[str, "SuffixTreeNode"]] = {}
        self.suffix_indices: List[int] = []


class CompressedSuffixTree:
    def __init__(self, text: str):
        self.text = text
        self.root = SuffixTreeNode()
        if text:
            for i in range(len(text)):
                self._insert_suffix(text[i:], i)

    def _common_prefix_length(self, a: str, b: str) -> int:
        length = 0
        limit = min(len(a), len(b))
        while length < limit and a[length] == b[length]:
            length += 1
        return length

    def _insert_suffix(self, suffix: str, index: int) -> None:
        node = self.root
        node.suffix_indices.append(index)
        remaining = suffix

        while remaining:
            first_char = remaining[0]

            if first_char not in node.children:
                leaf = SuffixTreeNode()
                leaf.suffix_indices.append(index)
                node.children[first_char] = (remaining, leaf)
                return

            edge_label, child = node.children[first_char]
            match_len = self._common_prefix_length(remaining, edge_label)

            if match_len == len(edge_label):
                node = child
                node.suffix_indices.append(index)
                remaining = remaining[match_len:]
            else:
                split_node = SuffixTreeNode()
                split_node.suffix_indices.extend(child.suffix_indices)
                split_node.suffix_indices.append(index)

                old_suffix = edge_label[match_len:]
                split_node.children[old_suffix[0]] = (old_suffix, child)

                new_suffix = remaining[match_len:]
                if new_suffix:
                    new_leaf = SuffixTreeNode()
                    new_leaf.suffix_indices.append(index)
                    split_node.children[new_suffix[0]] = (new_suffix, new_leaf)

                node.children[first_char] = (edge_label[:match_len], split_node)
                return

    def search(self, pattern: str) -> List[int]:
        """
        Return all start indices where pattern occurs.
        """
        if pattern == "":
            return list(range(len(self.text) + 1))

        node = self.root
        remaining = pattern

        while remaining:
            first_char = remaining[0]
            if first_char not in node.children:
                return []

            edge_label, child = node.children[first_char]
            match_len = self._common_prefix_length(remaining, edge_label)

            if match_len == len(remaining):
                return sorted(set(child.suffix_indices))
            if match_len < len(edge_label):
                return []
            node = child
            remaining = remaining[match_len:]

        return sorted(set(node.suffix_indices))

    def prefix_search(self, prefix: str) -> List[int]:
        """
        Alias for search in this suffix-based structure.
        """
        return self.search(prefix)

    def longest_repeated_substring(self) -> str:
        """
        Return one longest repeated substring in the text.
        """
        best = ""

        def dfs(node: SuffixTreeNode, path: str):
            nonlocal best
            if len(set(node.suffix_indices)) >= 2 and len(path) > len(best):
                best = path

            for _, (edge_label, child) in node.children.items():
                dfs(child, path + edge_label)

        dfs(self.root, "")
        return best

    def count_distinct_substrings(self) -> int:
        """
        Count distinct substrings via sum of edge lengths in compressed trie.
        """
        total = 0

        def dfs(node: SuffixTreeNode):
            nonlocal total
            for _, (edge_label, child) in node.children.items():
                total += len(edge_label)
                dfs(child)

        dfs(self.root)
        return total

    def edge_list(self) -> List[Tuple[str, str]]:
        """
        Return a simple list of edges for debugging/visualization.
        """
        edges = []

        def dfs(node: SuffixTreeNode, node_name: str):
            child_counter = 0
            for _, (edge_label, child) in node.children.items():
                child_name = f"{node_name}.{child_counter}"
                edges.append((node_name, f"{child_name}:{edge_label}"))
                dfs(child, child_name)
                child_counter += 1

        dfs(self.root, "root")
        return edges