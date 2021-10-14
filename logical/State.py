
import numpy as np

class QuantumState:
    def __init__(self, qubit_number):
        self.qubit_number = qubit_number
        self.statevector = 1
        self.build_state()

    def build_state(self):
        state_qubit = np.array([1,0])
        for idx in range(self.qubit_number):
            self.statevector = np.kron(self.statevector, state_qubit)