"""
@project: SDN-SR-TE
@author: sam
@file bandwidth_efficient_branch_aware_steiner_tree.py
@ide: PyCharm
@time: 2019-04-20 13:54:55
@blog: https://jiahaoplus.com
"""
from network import *
from algorithm.multicast_tree import *

__all__ = [
    'BandwidthefficientBranchawareSteinerTree'
]


class BandwidthefficientBranchawareSteinerTree(MulticastTree):

    def __init__(self, G, flows, **kwargs):
        super().__init__(G, flows, **kwargs)

        # Add node and edge weight
        nx.set_edge_attributes(self.graph, 0, 'weight')
        nx.set_node_attributes(self.graph, 0, 'weight')

        self.node_bc = nx.betweenness_centrality(self.graph)
        self.edge_bc = nx.edge_betweenness_centrality(self.graph)

        self.all_pair_paths = None

        self.deploy()

    def compute(self, source, destinations, **kwargs):
        """BBST
        :param source: The source of flow request
        :param destinations: The destinations of request
        :param kwargs:
        :return:
        """
        alpha = kwargs.get('alpha', 0.5)
        beta = kwargs.get('beta', 0.5)
        w1 = kwargs.get('w1', 1)
        w2 = kwargs.get('w2', 1)

        # Add weight for nodes and edges
        self.__generate_weighted_graph(alpha, beta)
        # Initialize T
        T = nx.Graph()
        T.add_node(source)
        T.root = source
        # Initialize terminals
        terminals = set(destinations)
        # Compute all pair weighted shortest paths
        self.all_pair_paths = dict(nx.all_pairs_dijkstra(self.graph,
                                                         weight='weight'))

        # While terminals isn't empty
        while terminals:
            # Initialize path
            path = None
            # Traverse all terminals
            for v in terminals:
                # Get the weighted shortest path from constructed tree to v
                p = self.__weighted_shortest_path_from_tree(v, T, w1, w2)
                # Update path
                if path is None or \
                        (path is not None and
                         self.__compute_extra_cost(T, p, w1, w2) <
                         self.__compute_extra_cost(T, path, w1, w2)):
                    path = p
            # Add path into T
            nx.add_path(T, path)
            # Remove the terminal node in current path
            terminals.remove(path[-1])

            # Remove the terminal already in T
            v_d = set()
            for v in terminals:
                if v in T.nodes:
                    v_d.add(v)
            terminals = terminals - v_d

        return T

    def __generate_weighted_graph(self, alpha, beta):
        """Generate the weighted graph according to the paper
        :param alpha: The parameter of edges for weight
        :param beta: The parameter of nodes for weight
        :return: weighted G
        """
        edges_data = []
        for e in self.graph.edges(data=True):
            # Compute the congestion for links
            congestion_index = self.graph.link_capacity / e[2][
                'residual_bandwidth']
            edges_data.append([congestion_index, self.edge_bc[(e[0], e[1])]])
        we = entropy(edges_data)

        for e in self.graph.edges(data=True):
            congestion_index = self.graph.link_capacity / e[2][
                'residual_bandwidth']
            e[2]['weight'] = (we[0] + alpha) * congestion_index + \
                             (we[1] + (1 - alpha)) * self.edge_bc[(e[0], e[1])]

        # Traverse the nodes
        nodes_data = []
        for v in self.graph.nodes(data=True):
            # Compute the congestion for nodes
            congestion_index = self.graph.flow_limit / v[1][
                'residual_flow_entries']
            nodes_data.append([congestion_index, self.node_bc[v[0]]])
        wv = entropy(nodes_data)

        for v in self.graph.nodes(data=True):
            # Compute the congestion for nodes
            congestion_index = self.graph.flow_limit / v[1][
                'residual_flow_entries'] - 1
            # Compute the weight according to the equation 4
            v[1]['weight'] = (wv[0] + beta) * congestion_index + \
                             (wv[1] + (1 - beta)) * self.node_bc[v[0]]


    def __compute_extra_cost(self, tree, path, w1, w2):
        """Compute the extra cost for path
        :param tree: The multicast tree
        :param path: The current path
        :param w1: The first parameter of extra cost
        :param w2: The second parameter of extra cost
        :return: extra_cost
        """
        # Compute the path cost
        extra_cost = w1 * self.all_pair_paths[path[0]][0][path[-1]]
        # Get the intersection
        intersection = path[0]
        # If intersection is new branch node, add cost of new branch node
        if (intersection == tree.root and tree.degree(intersection) == 1) or \
                (intersection != tree.root and tree.degree(intersection) == 2):
            extra_cost += w2 * self.graph.nodes[intersection]['weight']

        return extra_cost

    def __weighted_shortest_path_from_tree(self, target, tree, w1, w2):
        """Compute the weighted shortest path from constructed tree to target
        :param target: The target node needs to be added into the tree
        :param tree: The constructed tree
        :param w1: The weight parameter for extra path
        :param w2:The weight parameter for branch node
        :return: path
        """
        # Initialize path
        path = None
        # Traverse all nodes in tree
        for v in tree.nodes:
            # Get the weighted shortest path from v to target
            p = self.all_pair_paths[v][1][target]
            # Compute the sub path
            sub_path = acyclic_sub_path(tree, p)
            # Update path
            if path is None or (path is not None and
                                self.__compute_extra_cost(tree, sub_path, w1, w2) <
                                self.__compute_extra_cost(tree, path, w1, w2)):
                path = sub_path

        return path
