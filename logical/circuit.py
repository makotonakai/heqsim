from .gate import QuantumGate
import numpy as np
import ray
import sys
import os

from device.cluster import QuantumCluster

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
        qubit_num_on_each_device = [ray.get(processor.get_qubit_number.remote()) for processor in self.cluster.processor_list]
        if self.qubit_number > sum(qubit_num_on_each_device):
            print("The whole cluster needs more qubits or processors")
        else:
            
            qubit_num_on_circuit = self.qubit_number

            # 各デバイスのインデックスの個数を決定
            qubit_index_range_lists = []
            current_qubit_index = 0
            last_qubit_index = 0
            for device_index in range(len(qubit_num_on_each_device)):
                qubit_num_on_this_device = qubit_num_on_each_device[device_index]
                if qubit_num_on_this_device >=qubit_num_on_circuit:
                    last_qubit_index += qubit_num_on_circuit
                    qubit_index_list = [current_qubit_index, last_qubit_index]
                    qubit_index_range_lists.append(qubit_index_list)
                    break
                else:
                    last_qubit_index += qubit_num_on_this_device
                    qubit_num_on_circuit -= qubit_num_on_this_device
                    qubit_index_list = [current_qubit_index, last_qubit_index]
                    qubit_index_range_lists.append(qubit_index_list)
                    current_qubit_index = last_qubit_index

            qubit_index_lists = []
            for qubit_index_range in qubit_index_range_lists:
                [first, end] = qubit_index_range
                qubit_index_list = [num for num in range(self.qubit_number)][first:end]
                qubit_index_lists.append(qubit_index_list)

            # 各デバイスにインデックスを分配
            cluster = self.cluster
            for index in range(len(qubit_index_lists)):
                processor = cluster.processor_list[index]
                device_name = ray.get(processor.get_device_name.remote())
                cluster.index_dict[device_name] = qubit_index_lists[index]
            print(qubit_index_lists)
            return qubit_index_lists

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
        print(self.gate_list)

    def execute(self):
        self.allocate_index()
        # self.allocate_gate()
        # self.cluster.run_circuit()



    
    

        

