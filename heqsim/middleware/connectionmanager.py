
class ConnectionManager:

    def __init__(self, processor_list):

        self.processor_list = processor_list
        self.total_qubit_num = sum([processor.qubit_num for processor in self.processor_list])
        self.dict = {processor.id: [] for processor in self.processor_list}

    def initialize(self):
        for processor in self.processor_list:
            self.dict[processor.id] = [self.total_qubit_num, self.total_qubit_num + 1]
            self.total_qubit_num += 2

    def get_dict(self):
        return self.dict

    def add_qubit(self, processor_id, index):
        self.dict[processor_id].insert(index, self.total_qubit_num)
        self.total_qubit_num += 1

    def remove_qubit(self, processor_id, index):
        element = self.dict[processor_id][index]
        self.dict[processor_id].remove(element)

        for processor_id in list(self.dict.keys()):
            for index in range(len(self.dict[processor_id])):
                if self.dict[processor_id][index] > element:
                    self.dict[processor_id][index] -= 1
        self.total_qubit_num -= 1
