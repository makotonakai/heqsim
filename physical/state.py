
import numpy as np

class PhysicalState:
    def __init__(self, n):
        self.qubit_num = n
        self.statevector = 1
        self.build_state()

    def build_state(self):
        state_qubit = np.array([1,0])
        for idx in range(self.qubit_num):
            self.statevector = np.kron(self.statevector, state_qubit)

    def get_statevector(self):
        return self.statevector


