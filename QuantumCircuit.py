from QuantumGate import *
from QuantumState import *
import numpy as np


class QuantumCircuit:

    def __init__(self, n):
        self.n = n
        self.state = PhysicalState(self.n).statevector

    def x(self, idx):
        xmatrix = x_(self.n, idx)
        self.state = np.dot(xmatrix, self.state)

    def y(self, idx):
        ymatrix = y_(self.n, idx)
        self.state = np.dot(ymatrix, self.state)

    def z(self, idx):
        zmatrix = z_(self.n, idx)
        self.state = np.dot(zmatrix, self.state)

    def h(self, idx):
        hmatrix = h_(self.n, idx)
        self.state = np.dot(hmatrix, self.state)

    def cx(self, idx):
        cxmatrix = cx_(self.n, idx)
        self.state = np.dot(cxmatrix, self.state)
        

