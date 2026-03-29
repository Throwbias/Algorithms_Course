from src.flow.network import FlowNetwork


def test_add_edge_creates_forward_and_reverse_edges():
    network = FlowNetwork(3)
    network.add_edge(0, 1, 10)

    assert len(network.graph[0]) == 1
    assert len(network.graph[1]) == 1

    forward = network.graph[0][0]
    reverse = network.graph[1][0]

    assert forward.to == 1
    assert forward.capacity == 10
    assert forward.original_capacity == 10
    assert forward.is_reverse is False

    assert reverse.to == 0
    assert reverse.capacity == 0
    assert reverse.is_reverse is True


def test_add_flow_updates_residual_capacities():
    network = FlowNetwork(3)
    network.add_edge(0, 1, 10)

    network.add_flow(0, 0, 4)

    forward = network.graph[0][0]
    reverse = network.graph[1][0]

    assert forward.capacity == 6
    assert reverse.capacity == 4
    assert forward.flow == 4


def test_capacity_constraints_validation():
    network = FlowNetwork(2)
    network.add_edge(0, 1, 5)
    network.add_flow(0, 0, 3)

    assert network.validate_capacity_constraints() is True


def test_flow_conservation_validation():
    network = FlowNetwork(4)
    network.add_edge(0, 1, 5)
    network.add_edge(1, 2, 5)
    network.add_edge(2, 3, 5)

    network.add_flow(0, 0, 3)
    network.add_flow(1, 1, 3)
    network.add_flow(2, 1, 3)

    assert network.validate_flow_conservation(0, 3) is True