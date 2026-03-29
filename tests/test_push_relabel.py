from src.flow.network import FlowNetwork
from src.flow.push_relabel import push_relabel
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


def build_small_network():
    network = FlowNetwork(4)
    network.add_edge(0, 1, 3)
    network.add_edge(0, 2, 2)
    network.add_edge(1, 2, 1)
    network.add_edge(1, 3, 2)
    network.add_edge(2, 3, 4)
    return network


def test_push_relabel_max_flow_small_network():
    network = build_small_network()
    result = push_relabel(network, 0, 3)

    assert result["max_flow"] == 5
    assert result["push_count"] > 0
    assert result["discharge_count"] > 0


def test_push_relabel_matches_edmonds_karp():
    network_pr = build_clrs_style_network()
    network_ek = build_clrs_style_network()

    pr_result = push_relabel(network_pr, 0, 5)
    ek_result = edmonds_karp(network_ek, 0, 5)

    assert pr_result["max_flow"] == ek_result["max_flow"] == 23


def test_push_relabel_preserves_constraints():
    network = build_clrs_style_network()
    result = push_relabel(network, 0, 5)

    assert result["max_flow"] == network.total_flow_from_source(0)
    assert network.validate_capacity_constraints() is True
    assert network.validate_flow_conservation(0, 5) is True


def test_push_relabel_source_has_highest_initial_height():
    network = build_small_network()
    result = push_relabel(network, 0, 3)

    assert result["heights"][0] == network.num_vertices