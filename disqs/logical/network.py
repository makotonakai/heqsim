
import networkx as nx


class Network:
    def __init__(self):
        self.graph = nx.Graph()

    def add_link(self, node1, node2):
        self.graph.add_edge(node1, node2)

    def get_processor(self, id_):
        processor = None
        processor_list = self.get_processor_list()
        for p in processor_list:
            if p.id == id_:
                processor = p
                break
        return processor

    def get_processor_list(self):
        return list(self.graph.nodes)

    def get_link_id(self, source, target):
        link_list = self.get_link_list()
        if (source, target) in link_list:
            return link_list.index((source, target))
        else:
            return link_list.index((target, source))

    def get_link_list(self):
        return list(self.graph.edges)

    def get_link_num(self):
        return self.graph.number_of_edges()

    def set_node_id(self):
        for id_ in range(len(self.graph.nodes)):
            processor = list(self.graph.nodes)[id_]
            processor.set_id(id_)
