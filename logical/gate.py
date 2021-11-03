
class QuantumGate:
    def __init__(self, name, index, target_index=None):
        self.name = name
        self.index = index
        self.target_index = target_index

    def set_id(self, id_):
        self.id = id_

    def set_role(self, role):
        self.role = role

    def set_control_id(self, id_):
        self.control_id = id_

    def set_target_id(self, id_):
        self.target_id = id_
