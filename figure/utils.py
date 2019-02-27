"""
@project: RoutingAlgorithm
@author: sam
@file utils.py
@ide: PyCharm
@time: 2019-02-27 13:02:37
@blog: https://jiahaoplus.com
"""
import matplotlib.pyplot as plt
import networkx as nx
import random

POINT_MARKER = {'SPT': 'o', 'ST': 'v', 'WSPT': 's', 'WST': '*', 'BBSRT': 'D'}
POINT_COLOR = {'SPT': 'r', 'ST': 'm', 'WSPT': 'y', 'WST': 'g', 'BBSRT': 'b'}


def draw_topology(G, position, node_attribute=None, edge_attribute=None,
                  title="Test"):
    """Draw topology and save as png
    :param G: The graph
    :param position: The position of graph
    :param node_attribute: The node attribute correspond the node label,
     default None
    :param edge_attribute: The edge attribute correspond the edge label,
    default None
    :param title: The title of graph, default 'Test'
    :return:
    """
    # Set the figure size
    plt.figure(figsize=(15, 15))
    plt.title(title)
    # Draw the graph according to the position with labels
    nx.draw(G, position, with_labels=True)
    # Show the node labels
    nx.draw_networkx_labels(G, position,
                            labels=nx.get_node_attributes(G, node_attribute))
    # Show the edge labels
    nx.draw_networkx_edge_labels(G, position,
                                 edge_labels=nx.get_edge_attributes(
                                     G, edge_attribute))
    # Figure show
    plt.show()


def draw_results(results, x_label='Multigroup Size',
                 y_label='Number of Branch Node',
                 type='line'):
    """Draw results for main.py
    :param results: The final results as dict
    :param x_label: The x label of figure
    :param y_label: The y label of figure
    :param type: The figure type, including line and bar, default line
    :return:
    """
    # The figure size
    plt.figure(figsize=(9, 6))
    # Check the figure type
    if type == 'line':
        # Draw the line figure
        for key in results:
            plt.plot(*zip(*sorted(results[key].items())), label=key,
                     color=POINT_COLOR[key], marker=POINT_MARKER[key])

    elif type == 'bar':
        # Draw the bar figure
        # Get the x values
        x_value = list(results['SPT'].keys())
        # Compute the appropriate width
        width = (x_value[1] - x_value[0]) / 6
        # Initialize offset
        offset = list(range(len(results)))
        # Compute the offset
        for i in range(len(offset)):
            offset[i] -= (len(offset) - 1) / 2
        index = 0
        for key in results:
            # Compute the x value of each result
            x = list(results[key].keys())
            for i in range(len(x)):
                # The origin value plus the offset value
                x[i] += offset[index] * width
            plt.bar(x, list(results[key].values()), width=width,
                    label=key, color=POINT_COLOR[key])
            index += 1

    # Set the y line
    plt.grid(axis='y')
    # Set the legend
    plt.legend(bbox_to_anchor=(1.05, 0.4), loc=3, borderaxespad=0)
    # Set x and y labels
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    # Show the figure
    plt.show()


def generate_test_results():
    results = {'SPT': {}, 'ST': {}, 'WSPT': {}, 'WST': {}}

    for key in results:
        for index in range(10, 70, 10):
            results[key][index] = random.randint(10, 100)

    return results


def test():
    results = generate_test_results()
    draw_results(results, type='bar')
    # draw_results()


if __name__ == '__main__':
    test()
