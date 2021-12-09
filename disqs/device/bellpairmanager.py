
class BellPairManager:
    def __init__(self):
        self.remote_cnot_manager = {}

    def add_new_info(self, remote_cnot_info):
        remote_cnot_id = remote_cnot_info["id"]
        qubit_indices = remote_cnot_info["qubit_indices"]
        self.remote_cnot_manager[remote_cnot_id] = qubit_indices

    def get_info(self):
        return self.remote_cnot_manager

    def get_control_index(self, remote_cnot_id):
        index_list = self.remote_cnot_manager[remote_cnot_id]
        control_index = index_list[0]
        self.update(control_index)
        return control_index

    def get_target_index(self, remote_cnot_id):
        index_list = self.remote_cnot_manager[remote_cnot_id]
        target_index = index_list[0]
        self.update(target_index)
        return target_index

    def update(self, index):
        key = -1
        for key_ in list(self.remote_cnot_manager.keys()):
            if index in self.remote_cnot_manager[key_]:
                key = key_
        self.remote_cnot_manager[key].remove(index)

        key_list = list(self.remote_cnot_manager.keys())
        key_index = key_list.index(key)
        remaining_key_list = key_list[key_index:]

        for remaining_key in remaining_key_list:
            self.remote_cnot_manager[remaining_key] = [index - 1 for index in self.remote_cnot_manager[remaining_key]]
