
from PhysicalGate import *
from PhysicalState import *
import numpy as np


class PhysicalCircuit:

    def __init__(self, n):
        self.n = n
        self.state = PhysicalState(self.n).statevector

    def px(self, idx):
        xmatrix = px_(self.n, idx)
        self.state = np.dot(xmatrix, self.state)

    def py(self, idx):
        ymatrix = py_(self.n, idx)
        self.state = np.dot(ymatrix, self.state)

    def pz(self, idx):
        zmatrix = pz_(self.n, idx)
        self.state = np.dot(zmatrix, self.state)

    def ph(self, idx):
        hmatrix = ph_(self.n, idx)
        self.state = np.dot(hmatrix, self.state)

    def pcx(self, idx):
        cxmatrix = ph_(self.n, idx)
        self.state = np.dot(cxmatrix, self.state)

    
        
if __name__ == "__main__":
    
    pc = PhysicalCircuit(1)
    pc.py(0)
    print(pc.state)