from heqsim.software.gate import QuantumGate
from heqsim.software.network import Network
import networkx as nx


class GateAllocator:
    """A class for a module that allocate quantum gates in the program to each processor"""

    def __init__(self, gate_list, cluster, network):
        """Create a gate allocator

        Args:
            gate_list (list): A list of quantum gates
            cluster (Cluster): A cluster of physical quantum processors
        """
        self.gate_list = gate_list
        self.cluster = cluster
        self.network = network

    def set_network(self, network):
        """Set a new network to this gate allocator

        Args:
            network (Network): A network that connects quantum processors
        """
        self.network = network

    def get_processor_id_from_index_dict(self, index, index_dict):
        """Return a processor id that a particular qubit is allocated

        Args:
            index (int): A qubit index
            index_dict (dict): A dict that maps a processor id to a list of indices of allocated qubits

        Returns:
            int: A processor id that a particular qubit is allocated
        """
        processor_id = None
        for processor in list(index_dict.keys()):
            if index in index_dict[processor]:
                processor_id = processor
        return processor_id

    def set_gate_dict_to_cluster(self, gate_dict):
        """Set a gate dict to the cluster

        Args:
            gate_dict (dict): A dict that maps a processor id to a list of the allocated quantum gates
        """
        self.cluster.set_gate_dict(gate_dict)

    def is_neighboring(self, source_processor, target_processor):
        """Return whether the two given processors are neighbors

        Args:
            source_processor (QuantumProcessor): The source processor
            target_processor (QuantumProcessor): The target processor

        Returns:
            bool: Whether the two given processors are neighbors
        """
        path = nx.shortest_path(self.network.graph, source_processor, target_processor)
        if len(path) == 2:
            return True
        else:
            return False

    def make_connection(self, source_processor, target_processor):
        """Create a quantum connection between two quantum processors

        Args:
            source_processor (QuantumProcessor): The "sender" processor of a remote CNOT gate
            target_processor (QuantumProcessor): The "receiver" processor of a remote CNOT gate
        """

        if self.is_neighboring(source_processor, target_processor):

            source_id = source_processor.get_id()
            target_id = target_processor.get_id()
            link_id = self.network.get_link_id(source_processor, target_processor)

            self.gate_dict[source_id].append(QuantumGate("ENTANGLE", link_id=link_id, role="control"))
            self.gate_dict[target_id].append(QuantumGate("ENTANGLE", link_id=link_id, role="target"))

        else:
            path = nx.shortest_path(self.network.graph, source_processor, target_processor)
            middle_processor = path[-2]

            self.make_connection(source_processor, middle_processor)
            self.make_connection(middle_processor, target_processor)
            self.entanglement_swapping(source_processor, middle_processor, target_processor)

    def entanglement_swapping(self, source_processor, middle_processor, target_processor):
        """Perform the entanglement swapping

        Args:
            source_processor (QuantumProcessor): Source processor
            middle_processor (QuantumProcessor): The quantum processor that performs this entanglement swapping
            target_processor (QuantumProcessor): Target processor
        """
        middle_id = middle_processor.get_id()
        control_link_id = self.network.get_link_id(source_processor, middle_processor)
        target_link_id = self.network.get_link_id(middle_processor, target_processor)
        self.gate_dict[middle_id].append(QuantumGate("BELL_MEASURE", None, link_id=[control_link_id, target_link_id]))

    def execute(self, index_dict):
        """

        Args:
            index_dict (dict): A dict that maps a processor id to a list of the indices of allocated qubits
            network (Network): A network that connects quantum processors
        """
        self.processor_list = self.network.get_processor_list()
        self.gate_dict = {processor.id: [] for processor in self.processor_list}

        for gate in self.gate_list:

            for processor in self.processor_list:

                processor_id = processor.id

                # single qubit gate
                if gate.target_index is None:
                    if gate.index in index_dict[processor_id]:
                        self.gate_dict[processor_id].append(gate)

                # CNOT gates in the same processor
                elif gate.index in index_dict[processor_id] and gate.target_index in index_dict[processor_id]:
                    self.gate_dict[processor_id].append(gate)

                # Remote CNOT gates
                else:

                    # Add remote cnot to the controlled processor
                    if gate.index in index_dict[processor_id]:

                        source_id = self.get_processor_id_from_index_dict(gate.index, index_dict)
                        target_id = self.get_processor_id_from_index_dict(gate.target_index, index_dict)

                        source = self.network.get_processor(source_id)
                        target = self.network.get_processor(target_id)

                        self.make_connection(source, target)

                        # Forward path
                        processor_path = nx.shortest_path(self.network.graph, source, target)
                        link_id_path = []
                        for index in range(len(processor_path) - 1):
                            source_ = processor_path[index]
                            target_ = processor_path[index + 1]
                            link_id = self.network.get_link_id(source_, target_)
                            link_id_path.append(link_id)

                        for index in range(len(processor_path)):
                            processor = processor_path[index]
                            if processor.id == source_id:
                                link_id = link_id_path[0]
                                self.gate_dict[source_id].append(QuantumGate("FORWARD_CONTROL", gate.index, link_id=link_id))

                            elif processor.id == target_id:
                                link_id = link_id_path[-1]
                                self.gate_dict[target_id].append(QuantumGate("GET", link_id=link_id, role="control"))
                                self.gate_dict[target_id].append(QuantumGate("FORWARD_TARGET", target_index=gate.target_index, link_id=link_id))

                            else:
                                control_link_id = link_id_path[index - 1]
                                self.gate_dict[processor.id].append(QuantumGate("GET", link_id=control_link_id, role="control"))

                                target_link_id = link_id_path[index]
                                self.gate_dict[processor.id].append(QuantumGate("SEND", link_id=target_link_id, role="control"))

                        # Reverse path
                        reverse_processor_path = nx.shortest_path(self.network.graph, target, source)
                        reverse_link_id_path = []

                        for index in range(len(reverse_processor_path) - 1):
                            source_ = reverse_processor_path[index]
                            target_ = reverse_processor_path[index + 1]
                            link_id = self.network.get_link_id(source_, target_)
                            reverse_link_id_path.append(link_id)

                        for index in range(len(reverse_processor_path)):
                            processor = reverse_processor_path[index]
                            if processor.id == target_id:
                                link_id = reverse_link_id_path[0]
                                self.gate_dict[target_id].append(QuantumGate("BACKWARD_CONTROL", link_id=link_id))

                            elif processor.id == source_id:
                                link_id = reverse_link_id_path[-1]
                                self.gate_dict[source_id].append(QuantumGate("GET", link_id=link_id, role="target"))
                                self.gate_dict[source_id].append(QuantumGate("BACKWARD_TARGET", index=gate.index, link_id=link_id))

                            else:
                                control_link_id = reverse_link_id_path[index - 1]
                                self.gate_dict[processor.id].append(QuantumGate("GET", link_id=control_link_id, role="target"))

                                target_link_id = reverse_link_id_path[index]
                                self.gate_dict[processor.id].append(QuantumGate("SEND", link_id=target_link_id, role="target"))

        self.set_gate_dict_to_cluster(self.gate_dict)
