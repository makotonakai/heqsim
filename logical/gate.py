
class QuantumGate:
    def __init__(self, name, index, target_index=None):
        self.name = name
        self.index = index
        self.target_index = target_index


class RemoteCNOT(QuantumGate):
    def __init__(self, name, index, target_index, id_):
        super(RemoteCNOT, self).__init__(name, index, target_index)

        self.id_ = id_
        self.control_processor = None
        self.target_processor = None

    def set_control_processor(self, control_processor):
        self.control_processor = control_processor

    def set_target_processor(self, target_processor):
        self.target_processor = target_processor
