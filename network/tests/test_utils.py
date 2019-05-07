"""
@project: RoutingAlgorithm
@author: sam
@file test_utils.py
@ide: PyCharm
@time: 2019-03-04 17:57:41
@blog: https://jiahaoplus.com
"""
from network import *
from networkx.utils import pairwise
from algorithm.shortest_path_tree import *
import random


def test_1():
    """Test function draw_result
    :return:
    """
    def generate_test_result():
        result = {'SPT': {}, 'ST': {}, 'WSPT': {}, 'WST': {}}

        for key in result:
            for index in range(10, 70, 10):
                result[key][index] = random.randint(10, 100)
        return result

    results = generate_test_result()
    draw_result(results, 'x', 'y', type='bar')


def test_2():
    """Test function compute_throughput
    :return:
    """
    G = generate_topology(100)
    flows = generate_flow_requests(G, 1, 5, 100, 100)

    graph, allocated_flows, multicast_trees = \
        generate_shortest_path_trees(G, flows)

    assert compute_throughput(allocated_flows) == 500


def test_3():
    """Test function compute_num_branch_nodes
    :return:
    """
    T = nx.Graph()
    nx.add_path(T, [0, 1, 2, 3])

    multicast_trees = list([T])
    assert compute_num_branch_nodes(multicast_trees) == 0

    nx.add_path(T, [0, 1, 4])
    multicast_trees = list([T])
    assert compute_num_branch_nodes(multicast_trees) == 1

    nx.add_path(T, [0, 1, 5])
    multicast_trees = list([T])
    assert compute_num_branch_nodes(multicast_trees) == 1

    nx.add_path(T, [0, 1, 2, 6])
    multicast_trees = list([T])
    assert compute_num_branch_nodes(multicast_trees) == 2

    nx.add_path(T, [0, 1, 2, 6, 7])
    multicast_trees = list([T])
    assert compute_num_branch_nodes(multicast_trees) == 2

    nx.add_path(T, [0, 1, 4, 8])
    nx.add_path(T, [0, 1, 4, 9])
    multicast_trees = list([T])
    assert compute_num_branch_nodes(multicast_trees) == 3


def test_4():
    """Test function compute_path_minimum_bandwidth
    :return:
    """
    G = nx.Graph()
    G.add_edge(0, 1, residual_bandwidth=10)
    G.add_edge(1, 5, residual_bandwidth=5)
    G.add_edge(1, 2, residual_bandwidth=3)
    G.add_edge(1, 4, residual_bandwidth=6)
    G.add_edge(2, 3, residual_bandwidth=7)
    G.add_edge(2, 6, residual_bandwidth=1)
    G.add_edge(6, 7, residual_bandwidth=8)
    G.add_edge(4, 8, residual_bandwidth=20)
    G.add_edge(4, 9, residual_bandwidth=9)

    pos = graphviz_layout(G, prog='dot')
    draw_topology(G, pos, edge_attribute='residual_bandwidth')

    assert compute_path_minimum_bandwidth(G, [0, 1, 5]) == 5
    assert compute_path_minimum_bandwidth(G, [0, 1, 4, 9]) == 6
    assert compute_path_minimum_bandwidth(G, [0, 1, 4, 8]) == 6
    assert compute_path_minimum_bandwidth(G, [0, 1, 2, 3]) == 3
    assert compute_path_minimum_bandwidth(G, [0, 1, 2, 6]) == 1
    assert compute_path_minimum_bandwidth(G, [0, 1, 2, 6, 7]) == 1


def test_5():
    """Test function compute_path_cost
    :return:
    """
    G = nx.Graph()
    G.add_edge(0, 1, weight=10)
    G.add_edge(1, 5, weight=5)
    G.add_edge(1, 2, weight=3)
    G.add_edge(1, 4, weight=6)
    G.add_edge(2, 3, weight=7)
    G.add_edge(2, 6, weight=1)
    G.add_edge(6, 7, weight=8)
    G.add_edge(4, 8, weight=20)

    pos = graphviz_layout(G, prog='dot')
    draw_topology(G, pos, edge_attribute='weight')

    assert compute_path_cost(G, [0, 1, 2], 'weight') == 13
    assert compute_path_cost(G, [0, 1, 5], 'weight') == 15
    assert compute_path_cost(G, [0, 1, 2, 3], 'weight') == 20
    assert compute_path_cost(G, [0, 1, 2, 6], 'weight') == 14
    assert compute_path_cost(G, [0, 1, 2, 6, 7], 'weight') == 22
    assert compute_path_cost(G, [0, 1, 4], 'weight') == 16
    assert compute_path_cost(G, [0, 1, 4, 8], 'weight') == 36


def test_6():
    """Test function generate_k_shortest_path
    :return:
    """
    G = generate_topology(100)
    nx.set_edge_attributes(G, 0, 'weight')

    for e in G.edges(data=True):
        e[2]['weight'] = random.randint(10, 100)

    for _ in range(1 << 10):
        src, dst = random.sample(list(G.nodes), 2)
        paths = generate_k_shortest_paths(G, src, dst, k=5, weight='weight')

        for p1, p2 in pairwise(paths):
            assert compute_path_cost(G, p1, 'weight') <= \
                compute_path_cost(G, p2, 'weight')


@count_time
def test_7():
    """Test decorator count_time
    :return:
    """
    cnt = 1
    for i in range(1000):
        for j in range(1000):
            cnt += i + j


def test_8():
    """Test function compute_acyclic_sub_path
    :return:
    """
    T = nx.Graph()
    nx.add_path(T, [0, 1, 2, 3])
    nx.add_path(T, [0, 1, 2, 4])

    path = [0, 5, 2, 6]
    assert compute_acyclic_sub_path(T, path) == [2, 6]

    path = [0, 1, 2, 6]
    assert compute_acyclic_sub_path(T, path) == [2, 6]

    path = [0, 1, 2, 4, 6]
    assert compute_acyclic_sub_path(T, path) == [4, 6]

    path = [0, 4, 3, 6]
    assert compute_acyclic_sub_path(T, path) == [3, 6]

    path = [0, 5, 1, 6, 2, 7]
    assert compute_acyclic_sub_path(T, path) == [2, 7]
