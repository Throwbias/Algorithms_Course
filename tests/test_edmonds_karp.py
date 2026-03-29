from src.flow.network import FlowNetwork
from src.flow.edmonds_karp import edmonds_karp


def build_clrs_style_network():
    network = FlowNetwork(6)
    network.add_edge(0, 1, 16)
    network.add_edge(0, 2, 13)
    network.add_edge(1, 2, 10)
    network.add_edge(2, 1, 4)
    network.add_edge(1, 3, 12)
    network.add_edge(3, 2, 9)
    network.add_edge(2, 4, 14)
    network.add_edge(4, 3, 7)
    network.add_edge(3, 5, 20)
    network.add_edge(4, 5, 4)
    return network


def test_edmonds_karp_max_flow_small_network():
    network = build_clrs_style_network()
    result = edmonds_karp(network, 0, 5)

    assert result["max_flow"] == 23
    assert result["iterations"] > 0
    assert len(result["bottlenecks"]) == result["iterations"]
    assert len(result["augmenting_paths"]) == result["iterations"]


def test_edmonds_karp_preserves_constraints():
    network = build_clrs_style_network()
    result = edmonds_karp(network, 0, 5)

    assert result["max_flow"] == network.total_flow_from_source(0)
    assert network.validate_capacity_constraints() is True
    assert network.validate_flow_conservation(0, 5) is True


def test_edmonds_karp_single_path():
    network = FlowNetwork(3)
    network.add_edge(0, 1, 7)
    network.add_edge(1, 2, 5)

    result = edmonds_karp(network, 0, 2)

    assert result["max_flow"] == 5
    assert result["iterations"] == 1
    assert result["bottlenecks"] == [5]
    assert result["augmenting_paths"] == [[0, 1, 2]]