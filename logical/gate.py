
class QuantumGate:
    def __init__(self, name, index, target_index=None):
        self.name = name
        self.index = index
        self.target_index = target_index

    def set_index(self, new_index):
        self.index = new_index

    def set_target_index(self, new_index):
        self.target_index = new_index

    def set_control_processor(self, processor):
        self.control_processor = processor

    def set_target_processor(self, processor):
        self.target_processor = processor

    def set_id(self, id_):
        self.id = id_
