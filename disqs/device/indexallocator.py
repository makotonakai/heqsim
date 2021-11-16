
class IndexAllocator:
    def __init__(self, qubit_num, cluster):
        self.qubit_num = qubit_num
        self.cluster = cluster
        self.processor_list = self.cluster.processor_list

        self.set_qubit_dict()
        self.set_index_dict()

    def set_qubit_dict(self):
        self.qubit_dict = {self.get_id(processor): self.get_qubit_num(processor) for processor in self.processor_list}

    def set_index_dict(self):
        self.index_dict = {self.get_id(processor): [] for processor in self.processor_list}

    def set_index_dict_to_cluster(self):
        self.cluster.set_index_dict(self.index_dict)

    def get_id(self, processor):
        return self.cluster.get_id(processor)

    def get_qubit_num(self, processor):
        return self.cluster.get_qubit_num(processor)

    def execute(self):

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
