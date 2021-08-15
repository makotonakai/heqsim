
import numpy as np

class PhysicalState:
    def __init__(self, n):
        self.n = n
        self.state = 1
        self.BuildState()

    def BuildState(self):
        state_qubit = np.array([1,0])
        for idx in range(self.n):
            self.state = np.kron(self.state, state_qubit)

if __name__ == "__main__":

    state = PhysicalState(2)
    print(state.state)
