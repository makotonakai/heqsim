from Physical.Circuit import PhysicalCircuit
import sys
import os

class PhysicalProcessor:

    def __init__(self, QubitNumber=2, OneQubitGateTime=0.1, TwoQubitGateTime=0.2):
        self.QubitNumber = QubitNumber
        self.OneQubitGateTime = OneQubitGateTime
        self.TwoQubitGateTime = TwoQubitGateTime
        self.IndexList = []
        self.GateList = []
        self.pc = PhysicalCircuit(self.QubitNumber)