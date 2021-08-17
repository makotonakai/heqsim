
import numpy as np

class PhysicalState:
    def __init__(self, n):
        self.n = n
        self.statevector = 1
        self.BuildState()

    def BuildState(self):
        state_qubit = np.array([1,0])
        for idx in range(self.n):
            self.statevector = np.kron(self.statevector, state_qubit)

if __name__ == "__main__":

    state = PhysicalState(1)

