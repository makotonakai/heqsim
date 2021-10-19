
class IndexAllocator:
    def __init__(self, qubit_num, cluster):
        self.qubit_num = qubit_num
        self.cluster = cluster
        self.processor_dict = self.cluster.processor_dict
        self.allocated_result = {processor:[] for processor in self.processor_names()}

    def processor_names(self):
        return list(self.processor_dict.keys())

    def processor_num(self):
        return len(self.processor_dict)

    def execute(self):
        if self.qubit_num > self.cluster.total_qubit_num:
            raise Exception("You need to add more qubits to the quantum cluster")
        else:
            for qubit_i in range(self.qubit_num):
                processor_i = qubit_i % self.processor_num()
                processor_name = self.processor_names()[processor_i]
                qubits = self.processor_dict[processor_name]
                if qubits != 0:
                    self.allocated_result[processor_name].append(qubit_i)
                    self.processor_dict[processor_name] -= 1
                else:
                    del self.processor_dict[processor_name]
                    processor_i = (qubit_i+1) % self.processor_num()
                    processor_name = self.processor_names()[processor_i]
                    self.allocated_result[processor_name].append(qubit_i)
                    self.processor_dict[processor_name] -= 1

    def get_result(self):
        return self.allocated_result