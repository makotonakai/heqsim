
from .gate import *
from .state import PhysicalState
import numpy as np

class PhysicalCircuit:

    def __init__(self, n):
        self.qubit_num = n
        self.state = PhysicalState(self.qubit_num).get_statevector()

    def px(self, idx):
        xmatrix = px_(self.qubit_num, idx)
        self.state = np.dot(xmatrix, self.state)

    def py(self, idx):
        ymatrix = py_(self.qubit_num, idx)
        self.state = np.dot(ymatrix, self.state)

    def pz(self, idx):
        zmatrix = pz_(self.qubit_num, idx)
        self.state = np.dot(zmatrix, self.state)

    def ph(self, idx):
        hmatrix = ph_(self.qubit_num, idx)
        self.state = np.dot(hmatrix, self.state)

    def pcx(self, control_idx, target_idx):
        cxmatrix = pcx_(self.qubit_num, control_idx, target_idx)
        self.state = np.dot(cxmatrix, self.state)

    