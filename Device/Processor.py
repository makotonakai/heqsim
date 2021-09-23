from Physical.Circuit import PhysicalCircuit
import sys
import os

class QuantumProcessor:

    def __init__(self, device_name, qubit_number, single_qubit_gate_time, two_qubit_gate_time):
        self.device_name = device_name
        self.qubit_number = qubit_number
        self.single_qubit_gate_time = single_qubit_gate_time
        self.two_qubit_gate_time = two_qubit_gate_time
        self.index_list = []
        self.gate_lists = []
        self.pc = PhysicalCircuit(self.qubit_number)

    def add_new_zero(self, num, new_index):
        string = bin(num)[2:].zfill(self.qubit_number)
        string_list = list(string)
        string_list.insert(new_index, '0')
        new_string = "".join(string_list)
        return new_string

    def add_qubit(self, new_index):
        state_dict = {}
        for idx in range(len(self.pc.state)):
            new_idx = self.add_new_zero(idx, new_index)
            state_dict[new_idx] = self.pc.state[idx]

        new_state = [0 for idx in range(2**(self.qubit_number+1))]
        for key in list(state_dict.keys()):
            new_idx = int(key, 2)
            new_state[new_idx] = state_dict[key]
        self.pc.state = new_state
        return self.pc.state