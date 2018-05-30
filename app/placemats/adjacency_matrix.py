import networkx as nx
import logging
from itertools import combinations

logger = logging.getLogger(__name__)


def adjacency_matrix(edge_to_nodes: dict):
    graph = nx.Graph()
    for edge, nodes in edge_to_nodes.items():
        for n1, n2 in combinations(nodes, 2):
            if graph.has_edge(n1, n2):
                graph[n1][n2]['weight'] += 1
            else:
                graph.add_edge(n1, n2, weight=1)
    nodes = []
    node_to_index = {}
    idx = 0
    for n in graph.nodes:
        nodes.append({'name': n, 'group': 1})
        node_to_index[n] = idx
        idx += 1
    links = []
    for n1, n2, weight in graph.edges(data='weight'):
        links.append({
            'source': node_to_index[n1],
            'target': node_to_index[n2],
            'value': weight,
        })
    return {
        'nodes': nodes,
        'links': links,
    }
