
class IndexAllocator:
    def __init__(self, qubit_num, cluster):
        self.qubit_num = qubit_num
        self.cluster = cluster
        self.processor_list = self.cluster.processor_list

        self.set_qubit_dict()
        self.set_name_list()
        self.set_allocated_result()

    def set_qubit_dict(self):
        self.qubit_dict = {self.get_name(processor): self.get_qubit_num(processor) for processor in self.cluster.processor_list}

    def set_name_list(self):
        self.name_list = list(self.qubit_dict.keys())

    def set_allocated_result(self):
        self.allocated_result = {self.get_name(processor): [] for processor in self.cluster.processor_list}

    def get_name(self, processor):
        return self.cluster.get_name(processor)

    def get_qubit_num(self, processor):
        return self.cluster.get_qubit_num(processor)

    def execute(self):

        for qubit_i in range(self.qubit_num):
            processor_i = qubit_i % len(self.processor_list)
            processor_name = self.name_list[processor_i]
            qubits = self.qubit_dict[processor_name]
            if qubits != 0:
                self.allocated_result[processor_name].append(qubit_i)
                self.qubit_dict[processor_name] -= 1
            else:
                del self.qubit_dict[processor_name]
                processor_i = (qubit_i + 1) % len(self.processor_list)
                processor_name = self.name_list[processor_i]
                self.allocated_result[processor_name].append(qubit_i)
                self.qubit_dict[processor_name] -= 1

    def get_result(self):
        return self.allocated_result
