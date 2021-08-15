
import numpy as np

class PhysicalGate:

    def __init__(self):
        self.IMatrix = np.eye(2)
        self.Matrix = 1

    def xGate(self, n, idx):

        xMatrix = np.array([[0,1],[1,0]])

        for i in range(n):
            if i == idx:
                self.Matrix = np.kron(xMatrix, self.Matrix)
            else:
                self.Matrix = np.kron(self.IMatrix, self.Matrix)

        return self.Matrix

if __name__ == "__main__":

    gate = PhysicalGate()
    x = gate.xGate(2,0)
    print(x)