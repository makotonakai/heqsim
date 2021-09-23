from Logical.Gate import *
from Logical.State import QuantumState
import numpy as np
import sys
import os

from Device.Cluster import QuantumCluster

class QuantumCircuit:

    def __init__(self, qubit_number):
        self.qubit_number = qubit_number
        self.state = QuantumState(self.qubit_number).statevector
        self.cluster = QuantumCluster()
        self.cxgraph = {str(idx):[] for idx in range(self.qubit_number)}

    def x(self, idx):
        xmatrix = x_(self.qubit_number, idx)
        self.state = np.dot(xmatrix, self.state)

    def y(self, idx):
        ymatrix = y_(self.qubit_number, idx)
        self.state = np.dot(ymatrix, self.state)

    def z(self, idx):
        zmatrix = z_(self.qubit_number, idx)
        self.state = np.dot(zmatrix, self.state)

    def h(self, idx):
        hmatrix = h_(self.qubit_number, idx)
        self.state = np.dot(hmatrix, self.state)

    def cx(self, control_idx, target_idx):
        cxmatrix = cx_(self.qubit_number, control_idx, target_idx)
        self.state = np.dot(cxmatrix, self.state)
        self.cxgraph[str(control_idx)].append(str(target_idx))
        self.cxgraph[str(target_idx)].append(str(control_idx))
    
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

    def get_qubit_dict(self):
        processor_list = self.cluster.processor_list
        qubit_dict = {processor.device_name: processor.qubit_number for processor in processor_list}
        return qubit_dict

    def allocate_index(self):
        qubit_list = self.get_qubit_dict()
        print(qubit_list)
        # if self.qubit_number >= max(qubit_list):
        #     print("Allocate")
        # else:
        #     print("The whole quantum circuit can't be allocated on the whole cluster")
        #     print("Please add more qubits to at least one of the quantum processors")

    def allocate_gate(self):
        pass

    def get_new_state(self):
        cluster = QuantumCluster()
        new_state = cluster.add_qubit()
        return new_state


    
    

        

