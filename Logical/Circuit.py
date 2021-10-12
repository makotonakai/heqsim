from Logical.Gate import QuantumGate
from Logical.State import QuantumState
import numpy as np
import sys
import os

from Device.Cluster import QuantumCluster

class QuantumCircuit:

    def __init__(self, qubit_number):
        self.qubit_number = qubit_number
        self.cluster = QuantumCluster()
        self.index_dict = self.cluster.index_dict
        self.gate_dict = self.cluster.gate_dict
        self.cxgraph = self.cluster.cxgraph
        self.gate_list = []

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

    def allocate_index(self):
        qubit_num_list= [processor.qubit_number for processor in self.cluster.processor_list]
        answer_list = []
        if self.qubit_number > sum(qubit_num_list):
            print("The whole cluster needs more qubits or processors")
        else:
            first_end_list = []
            # 各デバイスのインデックスの個数を決定
            first = 0
            end = 0
            for num in qubit_num_list:
                if end > self.qubit_number:
                    end = self.qubit_number
                else:
                    end = first+num
                first_end_list.append([first, end])
                first = end
                if first == self.qubit_number:
                    first_end_list.append([first, self.qubit_number])

            # 各デバイスのインデックスを決定
            index_list = [num for num in range(self.qubit_number)]
            for first_end in first_end_list:
                [first, end] = first_end
                index = index_list[first:end]
                answer_list.append(index)

            # 各デバイスにインデックスを分配
            cluster = self.cluster
            for index in range(len(cluster.processor_list)):
                processor = cluster.processor_list[index]
                cluster.index_dict[processor.device_name] = answer_list[index]
            return answer_list

    def get_device_name(self, index):
        device_name = None
        for name in list(self.index_dict.keys()):
            if index in self.index_dict[name]:
                device_name = name
                break
            else:
                continue
        return device_name

    def allocate_gate(self):
        for gate in self.gate_list:
            name = self.get_device_name(gate.index)
            self.gate_dict[name].append(gate)

    def execute(self):
        self.allocate_index()
        self.allocate_gate()



    
    

        

