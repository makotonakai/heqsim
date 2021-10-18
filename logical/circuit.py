from .gate import QuantumGate
import numpy as np
import ray
import sys
import os

from device.cluster import QuantumCluster

class QuantumCircuit:

    def __init__(self, qubit_num):
        self.qubit_num = qubit_num
        self.cluster = QuantumCluster()

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
        self.cxgraph[str(control_idx)].append(str(target_idx))
        self.cxgraph[str(target_idx)].append(str(control_idx))

    def get_new_state(self):
        cluster = QuantumCluster()
        new_state = cluster.add_qubit()
        return new_state
    
    def qubit_contract(self, first_qubit_index, second_qubit_index):
        first_qubit_index = str(first_qubit_index)
        second_qubit_index = str(second_qubit_index)
        new_qubit_index = first_qubit_index + second_qubit_index
        
        self.cxgraph[new_qubit_index] = self.cxgraph[first_qubit_index]
        del self.cxgraph[first_qubit_index]

        for node in self.cxgraph.keys():
            if first_qubit_index in self.cxgraph[node]:
                for idx in range(len(self.cxgraph[node])):
                    if self.cxgraph[node][idx] == first_qubit_index:
                        self.cxgraph[node][idx] = new_qubit_index

        for node in self.cxgraph[second_qubit_index]:
            if node != new_qubit_index:
                self.cxgraph[new_qubit_index].append(node)
            self.cxgraph[node].remove(second_qubit_index)
            if node != new_qubit_index:
                self.cxgraph[node].append(new_qubit_index)
        del self.cxgraph[second_qubit_index]

        return new_qubit_index

    



    
    

        

