import pytest
from src.structures.avl_tree import AVLTree

@pytest.fixture
def sample_tree():
    tree = AVLTree()
    keys = [20, 4, 15, 70, 50, 100, 10]
    for key in keys:
        tree.insert(key)
    return tree

def test_insertion_in_order(sample_tree):
    """Test that in-order traversal returns sorted keys after insertion."""
    sorted_keys = sample_tree.in_order_traversal()
    assert sorted_keys == sorted(sorted_keys)

def test_search_existing_keys(sample_tree):
    """Test that inserted keys can be found."""
    for key in [20, 4, 70, 10]:
        assert sample_tree.search(key) is True

def test_search_non_existing_key(sample_tree):
    """Test that searching for a missing key returns False."""
    assert sample_tree.search(999) is False
    assert sample_tree.search(-5) is False

def test_delete_leaf_node(sample_tree):
    """Delete a leaf node and verify structure."""
    sample_tree.delete(10)
    assert sample_tree.search(10) is False
    sorted_keys = sample_tree.in_order_traversal()
    assert sorted_keys == sorted(sorted_keys)

def test_delete_node_one_child(sample_tree):
    """Delete a node with one child and verify structure."""
    sample_tree.delete(100)
    assert sample_tree.search(100) is False
    sorted_keys = sample_tree.in_order_traversal()
    assert sorted_keys == sorted(sorted_keys)

def test_delete_node_two_children(sample_tree):
    """Delete a node with two children and verify structure."""
    sample_tree.delete(20)
    assert sample_tree.search(20) is False
    sorted_keys = sample_tree.in_order_traversal()
    assert sorted_keys == sorted(sorted_keys)

def test_tree_height_balanced(sample_tree):
    """Verify height remains consistent with AVL balance."""
    # For n=7, max height should be <= log2(n) * 2 (loose upper bound)
    height = sample_tree.height()
    assert height <= 5  # AVL tree is balanced
