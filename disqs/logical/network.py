
import networkx as nx


class Network:
    def __init__(self):
        self.graph = nx.Graph()

    def add_link(self, node1, node2):
        self.graph.add_edge(node1, node2)

    def processor_list(self):
        return list(self.graph.nodes)

    def set_node_id(self):
        for id_ in range(len(self.graph.nodes)):
            processor = list(self.graph.nodes)[id_]
            processor.set_id(id_)
