
class QuantumProcessor:

    def __init__(self, qubit_num=1, execution_time=0.1):
        self.id = 0
        self.qubit_num = qubit_num
        self.execution_time = execution_time

    def set_id(self, id_):
        self.id = id_

    def get_info(self):
        info = {
            "id": self.id,
            "qubit_num": self.qubit_num,
            "execution_time": self.execution_time
        }
        return info
