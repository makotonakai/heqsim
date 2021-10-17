
class IndexAllocator:
    def __init__(self, qc, cluster):
        self.qc = qc
        self.cluster = cluster

    def get_qubit_number(self):
        return qc.qubit_number