
class IndexAllocator:
    def __init__(self, qubit_num, cluster):
        self.qubit_num = qubit_num
        self.cluster = cluster
        self.processor_list = self.cluster.processor_list

        self.set_qubit_dict()
        self.set_allocated_result()

    def set_qubit_dict(self):
        self.qubit_dict = {self.get_id(processor): self.get_qubit_num(processor) for processor in self.processor_list}

    def set_allocated_result(self):
        self.allocated_result = {self.get_id(processor): [] for processor in self.processor_list}

    def get_id(self, processor):
        return self.cluster.get_id(processor)

    def get_qubit_num(self, processor):
        return self.cluster.get_qubit_num(processor)

    def get_processor(self, id_):
        processor = None
        for processor_ in list(self.qubit_dict.keys()):
            if self.get_id(processor_) == id_:
                processor = processor_
        return processor

    def execute(self):

        for qubit_i in range(self.qubit_num):
            processor_i = qubit_i % len(self.processor_list)
            qubits = self.qubit_dict[processor_i]
            if qubits != 0:
                self.allocated_result[processor_i].append(qubit_i)
                self.qubit_dict[processor_i] -= 1
            else:
                del self.qubit_dict[processor_i]
                processor_i = (qubit_i + 1) % len(self.processor_list)
                self.allocated_result[processor_i].append(qubit_i)
                self.qubit_dict[processor_i] -= 1

    def get_result(self):
        return self.allocated_result
