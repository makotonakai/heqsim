
import networkx as nx


class Network:
    """A class for network that connects quantum processors"""

    def __init__(self):
        """Define a new network"""
        self.graph = nx.Graph()

    def add_link(self, node1, node2):
        """Add a new link to this network

        Args:
            node1 (QuantumProcessor): one quantum processor
            node2 (QuantumProcessor): the other quantum processor
        """
        self.graph.add_edge(node1, node2)

    def get_processor(self, id_):
        """Return quantum processor with a specific id

        Args:
            id_ (int): a quantum processor id

        Returns:
            QuantumProcessor: the specified quantum processor
        """
        processor = None
        processor_list = self.get_processor_list()
        for p in processor_list:
            if p.id == id_:
                processor = p
                break
        return processor

    def get_processor_list(self):
        """Return the list of quantum processors

        Returns:
            list: list of quantum processors
        """
        return list(self.graph.nodes)

    def get_link_id(self, source, target):
        """Return the id of a specific link

        Args:
            source (QuantumProcessor): one quantum processor
            target (QuantumProcessor): the other quantum processor

        Returns:
            int: a link id
        """
        link_list = self.get_link_list()
        if (source, target) in link_list:
            return link_list.index((source, target))
        else:
            return link_list.index((target, source))

    def get_link_list(self):
        """Return the list of links in this network

        Returns:
            list: list of links
        """
        return list(self.graph.edges)

    def get_link_num(self):
        """Return the number of links in this network

        Returns:
            [type]: number of links
        """
        return self.graph.number_of_edges()

    def set_node_id(self):
        """Assign id to each quantum processors in this network"""
        for id_ in range(len(self.graph.nodes)):
            processor = list(self.graph.nodes)[id_]
            processor.set_id(id_)

    def generate_distance_matrix(self):
        """Create a distance matrix in this network

        Returns:
            numpy.array: distance matrix
        """
        return nx.floyd_warshall_numpy(self.graph)
