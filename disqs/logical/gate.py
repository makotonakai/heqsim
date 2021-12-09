
class QuantumGate:
    def __init__(self, name, index, target_index=None):
        self.name = name
        self.index = index
        self.target_index = target_index

    def set_remote_cnot_id(self, remote_cnot_id):
        self.remote_cnot_id = remote_cnot_id

    def set_link_id(self, link_id):
        self.link_id = link_id

    def set_role(self, role):
        self.role = role
