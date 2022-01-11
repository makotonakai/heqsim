from heqsim.software.gate import QuantumGate
import networkx as nx


class GateAllocator:
    """A class for a module that allocate quantum gates in the program to each processor"""

    def __init__(self, gate_list, cluster):
        """Create a gate allocator

        Args:
            gate_list (list): A list of quantum gates
            cluster (Cluster): A cluster of physical quantum processors
        """
        self.gate_list = gate_list
        self.cluster = cluster
        self.remote_cnot_id = 0

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

    def execute(self, index_dict, network):
        """

        Args:
            index_dict (dict): A dict that maps a processor id to a list of the indices of allocated qubits
            network (Network): A network that connects quantum processors
        """
        self.processor_list = network.get_processor_list()
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

                        source = network.get_processor(source_id)
                        target = network.get_processor(target_id)

                        path = nx.shortest_path(network.graph, source=source, target=target)
                        id_path = [processor.id for processor in path]
                        id_path_reversed = list(reversed(id_path))
                        id_full_path = [id_path, "CNOT", id_path_reversed]

                        control_target_link_list = []
                        for id_path in id_full_path:
                            if id_path == "CNOT":
                                control_target_link_list.append("CNOT")
                            else:
                                for id_ in range(len(id_path) - 1):

                                    [control, target] = id_path[id_:id_ + 2]

                                    control_id_ = self.get_processor_id_from_index_dict(control, index_dict)
                                    target_id_ = self.get_processor_id_from_index_dict(target, index_dict)

                                    control_processor = network.get_processor(control_id_)
                                    target_processor = network.get_processor(target_id_)

                                    link = network.get_link_id(control_processor, target_processor)
                                    control_target_link = [control, target, link]

                                    control_target_link_list.append(control_target_link)

                        first_swap_gate = QuantumGate("SWAP", gate.index)
                        first_swap_gate.set_role("first")
                        self.gate_dict[source_id].append(first_swap_gate)

                        for control_target_link in control_target_link_list:

                            if control_target_link == "CNOT":
                                cnot_gate = QuantumGate("CNOT", None, gate.target_index)
                                cnot_gate.set_role("remote")
                                self.gate_dict[target_id].append(cnot_gate)
                            else:
                                [control, target, link] = control_target_link
                                [remote_cnot_control, remote_cnot_target] = [QuantumGate("RemoteCNOT", control, target) for _ in range(2)]

                                remote_cnot_control.set_role(["control", "forth"])
                                remote_cnot_target.set_role(["target", "forth"])

                                control_id_ = self.get_processor_id_from_index_dict(control, index_dict)
                                target_id_ = self.get_processor_id_from_index_dict(target, index_dict)

                                control_processor = network.get_processor(control_id_)
                                target_processor = network.get_processor(target_id_)

                                remote_cnot_control.set_remote_cnot_id(self.remote_cnot_id)
                                remote_cnot_target.set_remote_cnot_id(self.remote_cnot_id)
                                self.remote_cnot_id += 1

                                link_id = network.get_link_id(control_processor, target_processor)
                                remote_cnot_control.set_link_id(link_id)
                                remote_cnot_target.set_link_id(link_id)

                                control_id = control_processor.id
                                self.gate_dict[control_id].append(remote_cnot_control)

                                target_id = target_processor.id
                                self.gate_dict[target_id].append(remote_cnot_target)

                                if target == gate.index:
                                    swap_gate = QuantumGate("SWAP", gate.index)
                                    swap_gate.set_role("last")
                                    swap_gate.set_link_id(link)
                                    self.gate_dict[source_id].append(swap_gate)
                                else:
                                    swap_gate = QuantumGate("SWAP", None)
                                    swap_gate.set_role("intermit")
                                    swap_gate.set_link_id(link)
                                    self.gate_dict[target_id].append(swap_gate)

        self.set_gate_dict_to_cluster(self.gate_dict)
