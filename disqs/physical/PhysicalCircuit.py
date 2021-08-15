
import numpy as np
import PhysicalState

class PhysicalCircuit:

    def __init__(self,n):
        self.n = n
        self.state = PhysicalState(self.n).state

    def x(self, idx):
        xMatrix = np.array([[0,1],[1,0]])
        
