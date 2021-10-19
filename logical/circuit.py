from .gate import QuantumGate
from device.cluster import QuantumCluster
from device.indexallocator import IndexAllocator

import numpy as np
import sys
import os

class QuantumCircuit:

    def __init__(self, qubit_num):
        self.qubit_num = qubit_num
        self.cluster = QuantumCluster()
        self.index_allocator = IndexAllocator(self.qubit_num, self.cluster)

    def x(self, idx):
        self.gate_list.append(QuantumGate("X", idx))

    def y(self, idx):
        self.gate_list.append(QuantumGate("Y", idx))
        
    def z(self, idx):
        self.gate_list.append(QuantumGate("Z", idx))

    def h(self, idx):
        self.gate_list.append(QuantumGate("H", idx))

    def cx(self, control_idx, target_idx):
        self.gate_list.append(QuantumGate("CX", control_idx, target_idx))

    def get_indices(self):
        self.index_allocator.execute()
        result = self.index_allocator.get_result()
        return result
    
    



    
    

        

