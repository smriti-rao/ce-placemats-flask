import networkx as nx
import logging
from itertools import combinations

logger = logging.getLogger(__name__)

def hierarchical_data(edge_to_nodes: dict, node_whitelist: set=None):
    # Creating a graph of keywords
    graph = nx.Graph()
    keywords = []
    keyword_category_dict = defaultdict()


    for edges, nodes in edge_to_nodes.items():
        new_nodes = []
        for n in nodes:
            if n in keyword_category_dict:
                new_nodes.append(keyword_category_dict[n])
            else:
                renamed_node = get_mesh_category(n) + '.' + n
                renamed_node = renamed_node.replace(' and ','+')
                renamed_node = renamed_node.replace('_and_', '+')
                #renamed_node = renamed_node.replace(' ', '')
                new_nodes.append(renamed_node)
                keyword_category_dict[n] = renamed_node
        keywords.extend(new_nodes)
        for n1, n2 in combinations(new_nodes, 2):
            if node_whitelist is not None and (n1 not in node_whitelist or n2 not in node_whitelist):
                continue
            if graph.has_edge(n1, n2):
                graph[n1][n2]['weight'] += 1
            else:

                graph.add_edge(n1, n2, weight=1)

    print(keywords)

    co_occurences = []

    for n in graph.nodes:
        imports = []
        imports = [nb for nb in graph.neighbors(n)]
        co_occurences.append({'name': n, 'size': keywords.count(n), 'imports': imports})

    return co_occurences