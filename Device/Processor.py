import sys
import os

sys.path.append(os.path.abspath(".."))
from Physical.Circuit import *

class Processor:

    def __init__(self, QubitNumber=2, OneQubitGateTime=0.1, TwoQubitGateTime=0.2):
        self.QubitNumber = QubitNumber
        self.OneQubitGateTime = OneQubitGateTime
        self.TwoQubitGateTime = TwoQubitGateTime
        self.IndexList = []
        self.GateList = []
        self.pc = PhysicalCircuit(self.QubitNumber)

p = Processor()
print(p.QubitNumber)