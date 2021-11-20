
class IndexAllocator:
    def __init__(self, qubit_num, cluster):
        self.qubit_num = qubit_num
        self.cluster = cluster

    def set_index_dict_to_cluster(self):
        self.cluster.set_index_dict(self.index_dict)

    def execute(self, network):

        self.processor_list = network.processor_list()
        self.qubit_dict = {processor.id: processor.qubit_num for processor in self.processor_list}
        self.index_dict = {processor.id: [] for processor in self.processor_list}

        for qubit_i in range(self.qubit_num):
            processor_i = qubit_i % len(self.processor_list)
            qubits = self.qubit_dict[processor_i]
            if qubits != 0:
                self.index_dict[processor_i].append(qubit_i)
                self.qubit_dict[processor_i] -= 1
            else:
                del self.qubit_dict[processor_i]
                processor_i = (qubit_i + 1) % len(self.processor_list)
                self.index_dict[processor_i].append(qubit_i)
                self.qubit_dict[processor_i] -= 1

        self.set_index_dict_to_cluster()

    def get_result(self):
        return self.index_dict
