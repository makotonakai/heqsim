from heqsim.middleware.allocationoptimizer import AllocationOptimizer
import random


class IndexAllocator:
    """A class of module that allocates qubit indices in the program to physical quantum processors"""

    def __init__(self, qubit_num, cluster):
        """Create an index allocator

        Args:
            qubit_num (int): The total number of qubits in the program
            cluster (Cluster): A cluster of quantum processors
        """
        self.qubit_num = qubit_num
        self.cluster = cluster

    def set_index_dict_to_cluster(self):
        """Set an index dict to the cluster"""
        self.cluster.set_index_dict(self.index_dict)

    def execute(self, network, gate_list, is_optimized):
        """Execute index allocation

        Args:
            network (Network): A network that connects quantum processors
            gate_list (list): A list of quantum gates
            is_optimized (bool): whether index allocation process is optimized
        """
        self.processor_list = network.get_processor_list()
        self.qubit_dict = {processor.id: processor.qubit_num for processor in self.processor_list}
        self.index_dict = {processor.id: [] for processor in self.processor_list}

        index_list = [num for num in range(self.qubit_num)]
        random.shuffle(index_list)

        start = 0
        end = 0
        for processor_id in range(len(self.processor_list)):
            end += self.qubit_dict[processor_id]
            index = index_list[start:end]
            self.index_dict[processor_id] = index
            start = end

        if is_optimized:
            opt = AllocationOptimizer(network, gate_list)
            self.index_dict = opt.optimize(self.index_dict)

        self.set_index_dict_to_cluster()

    def get_result(self):
        """Return the result of index allocation

        Returns:
            dict: A dict that maps processor id to list of allocated quantum gates
        """
        return self.index_dict
